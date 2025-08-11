from pydantic import BaseModel


class Token(BaseModel):
    """Schema para resposta de autenticação com token JWT."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema para dados extraídos do token JWT."""
    username: str | None = None
