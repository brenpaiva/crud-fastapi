import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends

from app.db.session import engine, init_db
from app.api.routers.age_groups import router as age_groups_router
from app.api.routers.enrollments import router as enrollments_router
from app.utils.logger import configure_logging, logger


def create_app() -> FastAPI:
    """
    Cria e configura a instância FastAPI com rotas, autenticação e eventos de ciclo de vida.
    
    Returns:
        FastAPI: Aplicação configurada e pronta para uso
    """
    from fastapi.security import OAuth2PasswordRequestForm
    from app.core.security import authenticate_user, create_access_token
    from app.schemas.token_schema import Token
    from sqlmodel.ext.asyncio.session import AsyncSession
    from app.db.session import get_session
    from datetime import timedelta

    configure_logging()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """Gerencia o ciclo de vida da aplicação (startup/shutdown)."""
        logger.info("Application startup")
        if os.getenv("INIT_DB", "false").lower() == "true":
            logger.info("Initializing database schema")
            await init_db()
        yield
        logger.info("Application shutdown")

    app = FastAPI(
        title="Event Enrollment API",
        version="1.0.0",
        openapi_url="/api/v1/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    @app.post("/token", response_model=Token, tags=["auth"])
    async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_session)
    ):
        """Endpoint de autenticação que retorna token JWT."""
        is_auth = await authenticate_user(form_data.username, form_data.password, session)
        if not is_auth:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(
            data={"sub": form_data.username},
            expires_delta=timedelta(minutes=60)
        )
        return {"access_token": access_token, "token_type": "bearer"}

    app.include_router(age_groups_router)
    app.include_router(enrollments_router)

    @app.get("/", tags=["root"])
    async def root():
        """Endpoint principal com informações da API."""
        return {
            "message": "Bem-vindo à Event Enrollment API!",
            "docs": "/docs",
            "redoc": "/redoc"
        }

    @app.get("/api/v1/health", tags=["health"])
    async def health_check():
        """Health check que verifica conectividade com banco de dados."""
        try:
            async with engine.connect() as conn:
                await conn.execute("SELECT 1")
            return {"status": "ok"}
        except Exception as e:
            logger.error("Health check failed", error=str(e))
            return {"status": "error", "detail": str(e)}

    return app


app = create_app()
