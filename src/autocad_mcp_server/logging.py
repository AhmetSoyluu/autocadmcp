from __future__ import annotations

import logging
import sys

try:
    from loguru import logger as loguru_logger
except ImportError:
    loguru_logger = None


def configure_logging(level: str) -> None:
    if loguru_logger is not None:
        loguru_logger.remove()
        loguru_logger.add(
            sys.stderr,
            level=level.upper(),
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
            enqueue=False,
            backtrace=False,
            diagnose=False,
        )
        return

    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def get_logger():
    if loguru_logger is not None:
        return loguru_logger
    return logging.getLogger("autocadmcp")
