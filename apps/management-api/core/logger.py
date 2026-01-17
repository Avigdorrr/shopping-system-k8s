import logging
import sys
from core.config import settings


def get_logger(name: str):
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ],
        force=True
    )

    logger = logging.getLogger(name)
    return logger


logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
logging.getLogger("aiokafka").setLevel(logging.WARNING)
logging.getLogger("motor").setLevel(logging.WARNING)
