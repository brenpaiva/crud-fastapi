
from app.db.session import engine
from sqlmodel import SQLModel
# importa todos os seus modelos para que fiquem registrados no metadata
import app.models.age_group
import app.models.enrollment



import asyncio

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("🏗️ Tabelas criadas com sucesso!")

if __name__ == "__main__":
    asyncio.run(init_db())
