from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Cria o engine assíncrono para PostgreSQL
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # habilita logs das queries SQL
)

# Fabrica de sessões assíncronas
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

from typing import AsyncGenerator

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependência do FastAPI para fornecer uma sessão de banco de dados.
    Usa context manager para abrir e fechar automaticamente.
    """
    async with AsyncSessionLocal() as session:
        yield session

async def init_db() -> None:
    """
    Inicializa o banco criando todas as tabelas definidas nos models.
    Útil no startup (apenas em dev), mas em produção prefira migrações com Alembic.
    """
    async with engine.begin() as conn:
        # importa os models para registrar metadados
        from app.models import age_group  # noqa: F401
        from app.models import enrollment  # noqa: F401

        await conn.run_sync(SQLModel.metadata.create_all)
