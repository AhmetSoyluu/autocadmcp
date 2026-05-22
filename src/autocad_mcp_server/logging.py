from __future__ import annotations

import sys

from loguru import logger


def configure_logging(level: str) -> None:
    logger.remove()
    logger.add(
        sys.stderr,
        level=level.upper(),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        enqueue=False,
        backtrace=False,
        diagnose=False,
    )


def get_logger():
    return logger
