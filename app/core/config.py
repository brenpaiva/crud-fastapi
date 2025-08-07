from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # URL de conexão async para PostgreSQL (formato aceito pelo SQLAlchemy)
    DATABASE_URL: str = Field("postgresql+asyncpg://postgres:breno123@localhost:5432/fastapi", env="DATABASE_URL")
    # Credenciais para Basic Auth
    API_USERNAME: str = Field("admin", env="API_USERNAME")
    API_PASSWORD: str = Field("secret", env="API_PASSWORD")
    # Configuração de logging
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Instância com as configurações carregadas
settings = Settings()
