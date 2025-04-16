"""Location filtering utilities for company data."""

import logging
from typing import List, Optional, Dict, Any

logger = logging.getLogger(__name__)

class LocationFilter:
    """Filter companies based on geographic location."""
    
    def __init__(self, target_locations: List[str]):
        """
        Initialize with list of target locations (cities, regions, countries)
        
        Args:
            target_locations: List of location strings to match against
        """
        self.target_locations = [loc.lower() for loc in target_locations]
        self.location_cache = {}  # Cache to avoid repeated lookups
    
    def is_in_target_location(self, company_location: Optional[str]) -> bool:
        """
        Check if company's location matches target locations
        
        Args:
            company_location: Location string to check
            
        Returns:
            Boolean indicating if location matches any target location
        """
        if not company_location:
            return False
            
        company_location = company_location.lower()
        
        # Check cache first
        if company_location in self.location_cache:
            return self.location_cache[company_location]
        
        # Direct string match check
        for target in self.target_locations:
            if target in company_location or company_location in target:
                self.location_cache[company_location] = True
                return True
        
        # Add more sophisticated matching as needed
        # For now, use simple substring matching
        
        # No match found
        self.location_cache[company_location] = False
        return False
    
    def filter_companies(self, companies: List[Dict[str, Any]], 
                         location_field: str = 'headquarters') -> List[Dict[str, Any]]:
        """
        Filter a list of company dictionaries by location
        
        Args:
            companies: List of company data dictionaries
            location_field: Key in company dict containing location information
            
        Returns:
            Filtered list of companies in target locations
        """
        return [
            company for company in companies 
            if self.is_in_target_location(company.get(location_field))
        ] 