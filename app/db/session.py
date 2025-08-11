from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    connect_args={
        "server_settings": {
            "timezone": "UTC",
        }
    }
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

from typing import AsyncGenerator

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependência do FastAPI para fornecer uma sessão de banco de dados.
    
    Yields:
        AsyncSession: Sessão de banco configurada que é automaticamente fechada
    """
    async with AsyncSessionLocal() as session:
        yield session


async def init_db() -> None:
    """
    Inicializa o banco de dados criando todas as tabelas definidas nos models.
    
    Note:
        Em produção, prefira usar migrações com Alembic ao invés desta função.
    """
    async with engine.begin() as conn:
        from app.models import age_group
        from app.models import enrollment

        await conn.run_sync(SQLModel.metadata.create_all)
