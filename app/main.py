import os
from fastapi import FastAPI, Depends

from app.db.session import engine, init_db
from app.api.routers.age_groups import router as age_groups_router
from app.api.routers.enrollments import router as enrollments_router
from app.utils.logger import configure_logging, logger


def create_app() -> FastAPI:
    from fastapi.security import OAuth2PasswordRequestForm
    from app.core.security import authenticate_user, create_access_token
    from app.schemas.token_schema import Token
    from sqlmodel.ext.asyncio.session import AsyncSession
    from app.db.session import get_session
    from datetime import timedelta
    """
    Cria e configura a instância FastAPI, inclui rotas e eventos de ciclo de vida.
    """
    # Configura logging estruturado
    configure_logging()

    app = FastAPI(
        title="Event Enrollment API",
        version="1.0.0",
        openapi_url="/api/v1/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    @app.post("/token", response_model=Token, tags=["auth"])
    async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_session)
    ):
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
    # Incluir routers
    app.include_router(age_groups_router)
    app.include_router(enrollments_router)


    # Rota principal
    @app.get("/", tags=["root"])
    async def root():
        return {
            "message": "Bem-vindo à Event Enrollment API!",
            "docs": "/docs",
            "redoc": "/redoc"
        }

    # Health check endpoint
    @app.get("/api/v1/health", tags=["health"])
    async def health_check():
        """Verifica conexão com o banco de dados e fila"""
        try:
            async with engine.connect() as conn:
                await conn.execute("SELECT 1")
            return {"status": "ok"}
        except Exception as e:
            logger.error("Health check failed", error=str(e))
            return {"status": "error", "detail": str(e)}

    # Evento de startup
    @app.on_event("startup")
    async def on_startup():
        logger.info("Application startup")
        # Cria tabelas no dev se variável INIT_DB estiver habilitada
        if os.getenv("INIT_DB", "false").lower() == "true":
            logger.info("Initializing database schema")
            await init_db()

    return app


# Instância principal da aplicação
app = create_app()
