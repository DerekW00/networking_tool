"""SEC data collection module."""

import logging
import re
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

import pandas as pd
import requests
from tqdm import tqdm


logger = logging.getLogger(__name__)

# SEC API endpoints
SEC_ARCHIVES_URL = "https://www.sec.gov/Archives/edgar/daily-index"
SEC_FILINGS_URL = "https://www.sec.gov/Archives/edgar/data"


def collect(config: Dict[str, Any]) -> pd.DataFrame:
    """
    Collect company and funding data from SEC EDGAR database.
    
    Args:
        config: Configuration containing parameters.
        
    Returns:
        DataFrame containing the collected data.
    """
    start_date = config.get("start_date", datetime.now().replace(day=1))
    end_date = config.get("end_date", datetime.now())
    
    logger.info(f"Collecting SEC data from {start_date} to {end_date}")
    
    # Set user agent for SEC API (required)
    user_agent = config.get("sec_user_agent", "AutoOutreach 1.0")
    headers = {
        "User-Agent": user_agent
    }
    
    # Target specific filing types (e.g., S-1, 10-K, etc.)
    target_forms = config.get("sec_target_forms", ["S-1", "S-1/A", "10-K", "10-Q"])
    
    all_filings = []
    current_date = start_date
    
    # Iterate through each day in the date range
    while current_date <= end_date:
        year = current_date.strftime("%Y")
        quarter = f"QTR{(current_date.month - 1) // 3 + 1}"
        date_str = current_date.strftime("%Y%m%d")
        
        # Construct URL for the daily index
        daily_index_url = f"{SEC_ARCHIVES_URL}/{year}/{quarter}/master.{date_str}.idx"
        
        try:
            response = requests.get(daily_index_url, headers=headers)
            
            if response.status_code == 200:
                # Process the index file
                filings = _parse_idx_file(response.text, target_forms)
                all_filings.extend(filings)
                logger.debug(f"Found {len(filings)} relevant filings on {date_str}")
            elif response.status_code != 404:  # 404 is expected for weekends/holidays
                logger.warning(f"Failed to fetch SEC index for {date_str}: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching SEC data for {date_str}: {e}")
        
        # Move to the next day
        current_date = datetime.fromordinal(current_date.toordinal() + 1)
    
    logger.info(f"Collected {len(all_filings)} SEC filings")
    
    # Convert to DataFrame
    if all_filings:
        df = pd.DataFrame(all_filings)
        return df
    else:
        return pd.DataFrame()


def _parse_idx_file(content: str, target_forms: List[str]) -> List[Dict[str, Any]]:
    """Parse the SEC daily index file and extract relevant filings."""
    filings = []
    
    # Skip header lines
    lines = content.split("\n")
    data_start = False
    
    for line in lines:
        if "----------------" in line:
            data_start = True
            continue
            
        if not data_start or not line.strip():
            continue
            
        try:
            # Parse line based on fixed-width format
            cik = line[0:12].strip()
            company_name = line[12:74].strip()
            form_type = line[74:86].strip()
            filing_date = line[86:98].strip()
            file_name = line[98:].strip()
            
            if form_type in target_forms:
                filings.append({
                    "cik": cik,
                    "company_name": company_name,
                    "form_type": form_type,
                    "filing_date": filing_date,
                    "file_url": f"{SEC_FILINGS_URL}/{cik}/{file_name}",
                })
        except Exception as e:
            logger.warning(f"Error parsing SEC index line: {e}")
    
    return filings 