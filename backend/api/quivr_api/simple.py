import structlog

from quivr_api.logger import get_logger

logger = get_logger("quivr-api")

print(structlog.is_configured())

logger.info("test")
