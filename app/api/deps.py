from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_session
from app.core.security import authenticate_user

security = HTTPBasic()


async def get_current_user(
    credentials: HTTPBasicCredentials = Depends(security),
    session: AsyncSession = Depends(get_session),
) -> str:
    """
    Valida credenciais de usuário usando Basic Auth.
    
    Args:
        credentials: Credenciais HTTP Basic
        session: Sessão do banco de dados
        
    Returns:
        str: Nome do usuário autenticado
        
    Raises:
        HTTPException: Se as credenciais forem inválidas
    """
    username = credentials.username
    password = credentials.password
    valid = await authenticate_user(username, password, session)
    if not valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return username
