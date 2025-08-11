from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Configurações da aplicação com carregamento automático de variáveis de ambiente."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:breno123@localhost:5432/fastapi",
        alias="DATABASE_URL",
        description="URL async do banco"
    )
    API_USERNAME: str = Field(default="admin", alias="API_USERNAME")
    API_PASSWORD: str = Field(default="secret", alias="API_PASSWORD")
    LOG_LEVEL: str = Field(default="INFO", alias="LOG_LEVEL")

    def model_post_init(self, __context):
        """Inicialização pós-validação do modelo."""
        return super().model_post_init(__context)


settings = Settings()
