import logging
from pythonjsonlogger import jsonlogger
from app.core.config import settings


def configure_logging() -> None:
    root = logging.getLogger()
    root.setLevel(settings.log_level)
    if root.handlers:
        return

    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter("%(levelname)s %(name)s %(message)s")
    handler.setFormatter(formatter)
    root.addHandler(handler)