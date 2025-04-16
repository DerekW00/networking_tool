"""Logging utilities for AutoOutreach."""

import logging
import logging.config
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional


def configure_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
) -> None:
    """
    Configure logging for the application.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file, if None logs only to console
        log_format: Format string for log messages
    """
    handlers = {"console": {"class": "logging.StreamHandler", "stream": sys.stdout}}
    
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        handlers["file"] = {
            "class": "logging.FileHandler",
            "filename": str(log_path),
            "mode": "a",
        }
    
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": log_format,
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": handlers,
        "loggers": {
            "": {  # Root logger
                "handlers": list(handlers.keys()),
                "level": log_level,
                "propagate": True,
            },
            # Silence noisy libraries
            "requests": {"level": "WARNING"},
            "urllib3": {"level": "WARNING"},
        },
    }
    
    # Update handler formatters
    for handler in handlers.keys():
        handlers[handler]["formatter"] = "standard"
    
    logging.config.dictConfig(config)
    
    logger = logging.getLogger(__name__)
    logger.debug("Logging configured successfully") 