"""Storage utilities for saving collected data."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Union

import pandas as pd


logger = logging.getLogger(__name__)


def save_to_csv(df: pd.DataFrame, output_path: Path) -> None:
    """
    Save a DataFrame to CSV.
    
    Args:
        df: The DataFrame to save.
        output_path: Path where the CSV file will be saved.
    """
    if df.empty:
        logger.warning(f"No data to save to {output_path}")
        return
        
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"Saved {len(df)} records to {output_path}")


def save_to_json(data: Union[List, Dict], output_path: Path) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: The data to save (list or dictionary).
        output_path: Path where the JSON file will be saved.
    """
    if not data:
        logger.warning(f"No data to save to {output_path}")
        return
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Custom JSON serializer to handle datetime objects
    def json_serial(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")
    
    with open(output_path, 'w') as f:
        json.dump(data, f, default=json_serial, indent=2)
    
    # Determine record count for logging
    if isinstance(data, list):
        record_count = len(data)
    else:
        record_count = 1
        
    logger.info(f"Saved {record_count} records to {output_path}")


def save_to_parquet(df: pd.DataFrame, output_path: Path) -> None:
    """
    Save a DataFrame to Parquet format.
    
    Args:
        df: The DataFrame to save.
        output_path: Path where the Parquet file will be saved.
    """
    if df.empty:
        logger.warning(f"No data to save to {output_path}")
        return
        
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)
    logger.info(f"Saved {len(df)} records to {output_path}") 