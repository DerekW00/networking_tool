"""Crunchbase data collection module."""

import logging
import time
from datetime import datetime
from typing import Dict, List, Any

import pandas as pd
import requests
from tqdm import tqdm


logger = logging.getLogger(__name__)


def collect(config: Dict[str, Any]) -> pd.DataFrame:
    """
    Collect company and funding data from Crunchbase.
    
    Args:
        config: Configuration containing API keys and parameters.
        
    Returns:
        DataFrame containing the collected data.
    """
    api_key = config.get("crunchbase_api_key")
    if not api_key:
        logger.error("No Crunchbase API key provided in config")
        raise ValueError("Crunchbase API key is required")
    
    start_date = config.get("start_date", datetime.now().replace(day=1))
    end_date = config.get("end_date", datetime.now())
    
    logger.info(f"Collecting Crunchbase data from {start_date} to {end_date}")
    
    # Construct API endpoint URL
    base_url = "https://api.crunchbase.com/api/v4/organizations/search"
    
    # Prepare search parameters
    params = {
        "user_key": api_key,
        "updated_since": start_date.strftime("%Y-%m-%d"),
        "updated_before": end_date.strftime("%Y-%m-%d"),
        "limit": 100,  # Maximum allowed by Crunchbase API
    }
    
    all_results = []
    page = 1
    
    # Paginate through results
    while True:
        logger.debug(f"Fetching page {page} from Crunchbase API")
        params["page"] = page
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            items = data.get("data", {}).get("items", [])
            
            if not items:
                break
                
            all_results.extend(items)
            logger.debug(f"Fetched {len(items)} items from page {page}")
            
            if len(items) < params["limit"]:
                break
                
            page += 1
            
            # Respect API rate limits
            time.sleep(1)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching Crunchbase data: {e}")
            break
    
    logger.info(f"Collected {len(all_results)} records from Crunchbase")
    
    # Process the results into a DataFrame
    if all_results:
        df = pd.json_normalize(all_results)
        
        # Perform any necessary transformations
        if "properties.funding_total.value_usd" in df.columns:
            df["funding_total_usd"] = df["properties.funding_total.value_usd"]
        
        if "properties.short_description" in df.columns:
            df["description"] = df["properties.short_description"]
        
        return df
    else:
        return pd.DataFrame() 