import logging
import sys
import structlog
from app.core.config import settings


def configure_logging() -> None:
    """
    Configura o logging estruturado usando structlog.
    
    Utiliza o nível de log definido nas configurações e formata
    as mensagens em JSON para facilitar a análise de logs.
    """
    log_level = settings.LOG_LEVEL if hasattr(settings, 'LOG_LEVEL') else 'INFO'
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )

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


logger = structlog.get_logger()  
