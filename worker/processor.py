"""
Worker para processamento assíncrono de enrollments usando Redis.

Este módulo implementa um worker que processa inscrições em lote,
aplicando regras de negócio e atualizando status no banco de dados.
"""

import asyncio
import os
import signal
from datetime import datetime, UTC
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from sqlmodel.ext.asyncio.session import AsyncSession

from app.queue.redis_backend import redis_queue
from app.db.session import engine
from app.models.enrollment import Enrollment, EnrollmentStatus
from app.utils.logger import configure_logging, logger


BATCH_SIZE = int(os.getenv("ENROLLMENT_WORKER_BATCH", "20"))
IDLE_BACKOFF = float(os.getenv("ENROLLMENT_WORKER_IDLE_BACKOFF", "2"))


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Fornece uma sessão de banco para o worker."""
    async_session = AsyncSession(engine, expire_on_commit=False)
    try:
        yield async_session
    finally:
        await async_session.close()


def apply_business_rules(enrollment: Enrollment) -> EnrollmentStatus:
    """
    Aplica regras de negócio para determinar o status da inscrição.
    
    Args:
        enrollment: Inscrição a ser avaliada
        
    Returns:
        EnrollmentStatus: Novo status da inscrição
        
    Note:
        Implementação atual sempre aprova. Expanda conforme necessário.
    """
    return EnrollmentStatus.approved


async def process_batch(session: AsyncSession) -> int:
    """
    Processa um lote de inscrições da fila Redis.
    
    Args:
        session: Sessão do banco de dados
        
    Returns:
        int: Número de inscrições processadas
    """
    jobs = await redis_queue.dequeue_batch(BATCH_SIZE)
    if not jobs:
        return 0
        
    processed = 0
    for job in jobs:
        enrollment_id = job.get("enrollment_id") if isinstance(job, dict) else None
        if not enrollment_id:
            continue
            
        enrollment = await session.get(Enrollment, enrollment_id)
        if not enrollment:
            logger.warning("Enrollment not found for job", enrollment_id=enrollment_id)
            continue
            
        if enrollment.status != EnrollmentStatus.pending:
            continue
            
        new_status = apply_business_rules(enrollment)
        enrollment.status = new_status
        enrollment.processed_at = datetime.now(UTC)
        session.add(enrollment)
        processed += 1
        
    if processed:
        await session.commit()
    return processed


class Worker:
    """Worker assíncrono para processar filas de inscrições."""
    
    def __init__(self):
        self._stop = asyncio.Event()

    def request_shutdown(self):
        """Solicita parada graceful do worker."""
        logger.info("Shutdown signal received")
        self._stop.set()

    async def run(self):
        """
        Loop principal do worker.
        
        Processa lotes de inscrições continuamente até receber
        sinal de parada.
        """
        configure_logging()
        logger.info("Enrollment worker started", batch_size=BATCH_SIZE)
        
        while not self._stop.is_set():
            try:
                async with get_session() as session:
                    processed = await process_batch(session)
                    
                if processed:
                    logger.info("Processed enrollments", count=processed)
                    await asyncio.sleep(0)
                else:
                    await asyncio.wait_for(self._stop.wait(), timeout=IDLE_BACKOFF)
                    
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error("Worker iteration error", error=str(e))
                await asyncio.sleep(2)
                
        logger.info("Enrollment worker stopping")


async def main():
    """Função principal que configura e executa o worker."""
    worker = Worker()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, worker.request_shutdown)
    await worker.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
