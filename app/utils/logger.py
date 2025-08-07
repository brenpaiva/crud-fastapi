import logging
import sys
import structlog
from app.core.config import settings


def configure_logging() -> None:
    """
    Configura o logging estruturado usando structlog e o módulo nativo logging.
 
    """
    # Configuração básica do logging nativo
    log_level = settings.LOG_LEVEL if hasattr(settings, 'LOG_LEVEL') else 'INFO'
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )

    # Configuração do structlog
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="ISO"),
            structlog.processors.add_log_level,
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


# Logger global
logger = structlog.get_logger()  
