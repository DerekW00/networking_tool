"""Tests for the collector configuration module."""

import os
import tempfile
from pathlib import Path

import pytest
import yaml

from collector.config import load_config


def test_load_config_with_file():
    """Test loading configuration from a file."""
    # Create a temporary config file
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".yaml") as temp_config:
        config_data = {
            "crunchbase_api_key": "test_key",
            "sec_user_agent": "Test Agent",
            "sources": {
                "crunchbase": {"enabled": True},
                "sec": {"enabled": False}
            }
        }
        yaml.dump(config_data, temp_config)
        temp_config.flush()
        
        # Load the config
        config = load_config(temp_config.name)
        
        # Verify loaded config
        assert config["crunchbase_api_key"] == "test_key"
        assert config["sec_user_agent"] == "Test Agent"
        assert config["sources"]["crunchbase"]["enabled"] is True
        assert config["sources"]["sec"]["enabled"] is False


def test_load_config_file_not_found():
    """Test error handling when config file is not found."""
    with pytest.raises(FileNotFoundError):
        load_config("nonexistent_file.yaml") 