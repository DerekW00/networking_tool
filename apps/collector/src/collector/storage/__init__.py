"""Storage utilities for saving collected data."""

import logging
from pathlib import Path

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