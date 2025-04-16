"""Collector CLI entrypoint."""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

import pandas as pd

from collector.config import load_config
from collector.sources import crunchbase, sec
from collector.storage import save_to_csv, save_to_json, save_to_parquet
from collector.filters import LocationFilter
from collector.extractors import DecisionMakerExtractor


logger = logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Collect company and funding data")
    parser.add_argument(
        "--config",
        type=str,
        help="Path to config file",
        default=None,
    )
    parser.add_argument(
        "--start-date",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d"),
        help="Start date for data collection (YYYY-MM-DD)",
        default=None,
    )
    parser.add_argument(
        "--end-date",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d"),
        help="End date for data collection (YYYY-MM-DD)",
        default=None,
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Directory to save output files",
        default=None,
    )
    parser.add_argument(
        "--target-locations",
        type=str,
        nargs="+",
        help="Target locations to filter companies by",
        default=None,
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the logging level",
    )
    return parser.parse_args()


def setup_logging(level):
    """Configure logging."""
    logging.basicConfig(
        level=getattr(logging, level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def filter_df_by_location(df: pd.DataFrame, location_filter: LocationFilter) -> pd.DataFrame:
    """
    Filter DataFrame by location
    
    Args:
        df: DataFrame to filter
        location_filter: LocationFilter instance
        
    Returns:
        Filtered DataFrame
    """
    if df.empty:
        return df
        
    # Determine location column based on DataFrame structure
    location_col = None
    potential_cols = ['headquarters', 'hq_location', 'location', 'city', 'address']
    for col in potential_cols:
        if col in df.columns:
            location_col = col
            break
    
    if not location_col:
        logger.warning("No location column found for location filtering")
        return df
        
    # Apply filter
    mask = df[location_col].apply(lambda loc: location_filter.is_in_target_location(loc))
    filtered_df = df[mask]
    logger.info(f"Filtered {len(df)} companies down to {len(filtered_df)} based on location")
    return filtered_df


def extract_decision_makers_from_dfs(dfs: List[pd.DataFrame]) -> List[Dict[str, Any]]:
    """
    Extract decision makers from a list of DataFrames
    
    Args:
        dfs: List of company DataFrames
        
    Returns:
        List of companies with decision makers
    """
    extractor = DecisionMakerExtractor()
    companies_with_decision_makers = []
    
    for df in dfs:
        if df.empty:
            continue
            
        for _, company in df.iterrows():
            company_dict = company.to_dict()
            decision_makers = extractor.extract_decision_makers(company_dict)
            
            if decision_makers:
                companies_with_decision_makers.append({
                    'company': company_dict,
                    'decision_makers': decision_makers
                })
    
    logger.info(f"Found {len(companies_with_decision_makers)} companies with decision makers")
    return companies_with_decision_makers


def main():
    """Execute the collector pipeline."""
    args = parse_args()
    setup_logging(args.log_level)
    
    logger.info("Starting data collection")
    
    try:
        config = load_config(args.config)
        
        # Override config with command line arguments
        if args.start_date:
            config["start_date"] = args.start_date
        if args.end_date:
            config["end_date"] = args.end_date
        if args.output_dir:
            config["output_dir"] = args.output_dir
        if args.target_locations:
            config["target_locations"] = args.target_locations
            
        # Initialize location filter from config
        target_locations = config.get("target_locations", [])
        if target_locations:
            logger.info(f"Filtering companies by locations: {', '.join(target_locations)}")
            location_filter = LocationFilter(target_locations)
        else:
            logger.info("No target locations specified, skipping location filtering")
            location_filter = None
            
        # Collect data from sources
        logger.info("Collecting data from Crunchbase")
        crunchbase_data = crunchbase.collect(config)
        
        logger.info("Collecting data from SEC")
        sec_data = sec.collect(config)
        
        # Filter by location if target locations are specified
        if location_filter and not target_locations:
            filtered_crunchbase = crunchbase_data
            filtered_sec = sec_data
        else:
            filtered_crunchbase = filter_df_by_location(crunchbase_data, location_filter)
            filtered_sec = filter_df_by_location(sec_data, location_filter)
        
        # Extract decision makers
        companies_with_decision_makers = extract_decision_makers_from_dfs(
            [filtered_crunchbase, filtered_sec]
        )
        
        # Save collected data
        output_dir = Path(config.get("output_dir", "../../data/raw"))
        output_dir.mkdir(parents=True, exist_ok=True)
        
        interim_dir = Path(config.get("interim_dir", "../../data/interim"))
        interim_dir.mkdir(parents=True, exist_ok=True)
        
        # Save raw data
        save_to_csv(crunchbase_data, output_dir / "crunchbase_data.csv")
        save_to_csv(sec_data, output_dir / "sec_data.csv")
        
        # Save filtered data
        save_to_csv(filtered_crunchbase, interim_dir / "filtered_crunchbase_data.csv")
        save_to_csv(filtered_sec, interim_dir / "filtered_sec_data.csv")
        
        # Save companies with decision makers
        save_to_json(
            companies_with_decision_makers, 
            interim_dir / "companies_with_decision_makers.json"
        )
        
        logger.info("Data collection completed successfully")
        return 0
    
    except Exception as e:
        logger.error(f"Error during data collection: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main()) 