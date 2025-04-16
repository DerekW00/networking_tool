"""Configuration loading utilities."""

import logging
import os
from pathlib import Path
from typing import Dict, Any

import yaml


logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATHS = [
    Path("../../configs/dev/collector.yaml"),
    Path("/etc/autooutreach/collector.yaml"),
    Path(os.path.expanduser("~/.config/autooutreach/collector.yaml")),
]


def load_config(config_path: str = None) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    
    Args:
        config_path: Path to the config file. If None, default locations will be checked.
        
    Returns:
        Dictionary containing configuration settings.
        
    Raises:
        FileNotFoundError: If no config file could be found.
    """
    if config_path:
        config_file = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        logger.info(f"Loading config from {config_path}")
        with open(config_file, "r") as f:
            return yaml.safe_load(f)
    
    # Try default config locations
    for path in DEFAULT_CONFIG_PATHS:
        if path.exists():
            logger.info(f"Loading config from {path}")
            with open(path, "r") as f:
                return yaml.safe_load(f)
    
    # If we get here, no config file was found
    raise FileNotFoundError(
        "No config file found. Please specify a config file with --config."
    ) 