
from app.core.config import settings
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime, timedelta, UTC
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas.token_schema import TokenData

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


async def authenticate_user(username: str, password: str, session: AsyncSession) -> bool:
    """
    Autentica um usuário verificando as credenciais contra as configurações.
    
    Args:
        username: Nome de usuário
        password: Senha do usuário  
        session: Sessão do banco de dados (não utilizada nesta implementação simples)
        
    Returns:
        bool: True se as credenciais são válidas, False caso contrário
    """
    if username == settings.API_USERNAME and password == settings.API_PASSWORD:
        return True
    return False


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Cria um token JWT de acesso com expiração configurável.
    
    Args:
        data: Dados a serem codificados no token
        expires_delta: Tempo de expiração personalizado (opcional)
        
    Returns:
        str: Token JWT codificado
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Valida o token JWT e retorna o usuário atual.
    
    Args:
        token: Token JWT fornecido no header Authorization
        
    Returns:
        str: Nome do usuário autenticado
        
    Raises:
        HTTPException: Se o token for inválido ou expirado
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    if username != settings.API_USERNAME:
        raise credentials_exception
    return username
