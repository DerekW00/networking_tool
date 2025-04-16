"""Collector CLI entrypoint."""

import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path

from collector.config import load_config
from collector.sources import crunchbase, sec
from collector.storage import save_to_csv


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
            
        # Collect data from sources
        logger.info("Collecting data from Crunchbase")
        crunchbase_data = crunchbase.collect(config)
        
        logger.info("Collecting data from SEC")
        sec_data = sec.collect(config)
        
        # Save collected data
        output_dir = Path(config.get("output_dir", "../../data/raw"))
        output_dir.mkdir(parents=True, exist_ok=True)
        
        save_to_csv(crunchbase_data, output_dir / "crunchbase_data.csv")
        save_to_csv(sec_data, output_dir / "sec_data.csv")
        
        logger.info("Data collection completed successfully")
        return 0
    
    except Exception as e:
        logger.error(f"Error during data collection: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main()) 