"""
Trust Labs Analytics — Structured Logging Configuration
"""

import logging
import logging.handlers
import os
import sys
from pathlib import Path


def setup_logging(
    log_dir: str = "logs",
    app_level: int = logging.INFO,
    max_bytes: int = 5 * 1024 * 1024,  # 5 MB
    backup_count: int = 3,
) -> logging.Logger:
    """Configure application logging with rotation.

    Args:
        log_dir: Directory for log files (created if missing).
        app_level: Logging level for the application logger.
        max_bytes: Maximum size of a single log file before rotation.
        backup_count: Number of rotated log files to keep.

    Returns:
        Configured root application logger.
    """
    # Ensure log directory exists
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("trust_labs")
    logger.setLevel(app_level)

    # Avoid duplicate handlers if setup_logging is called multiple times
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s — %(name)s — %(levelname)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Rotating file handler
    file_handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(log_dir, "app.log"),
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setLevel(app_level)
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(app_level)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info("Logging initialized — trust_labs")
    return logger


def get_logger(name: str = "trust_labs") -> logging.Logger:
    """Return a named logger child of the trust_labs hierarchy."""
    return logging.getLogger(name)
