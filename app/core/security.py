from app.core.config import settings
from sqlmodel.ext.asyncio.session import AsyncSession


async def authenticate_user(
    username: str,
    password: str,
    session: AsyncSession
) -> bool:
    """
    Verifica usuário e senha contra valores estáticos definidos em config.
    Em produção, substitua por consulta na tabela de usuários.
    """
    # Comparação simples (não-hashed) para demonstração
    if username == settings.API_USERNAME and password == settings.API_PASSWORD:
        return True
    return False
