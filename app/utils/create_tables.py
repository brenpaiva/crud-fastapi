
import asyncio
from app.db.session import engine
from sqlmodel import SQLModel
import app.models.age_group
import app.models.enrollment


async def init_db():
    """
    Inicializa o banco de dados criando todas as tabelas definidas nos modelos.
    
    Esta função é útil para desenvolvimento e testes. Em produção,
    prefira usar migrações com Alembic.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("🏗️ Tabelas criadas com sucesso!")


if __name__ == "__main__":
    asyncio.run(init_db())
