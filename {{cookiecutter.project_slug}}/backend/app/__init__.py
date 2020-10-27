import logging.config

from app.core.config import settings

logging.config.dictConfig(settings.LOGGING)