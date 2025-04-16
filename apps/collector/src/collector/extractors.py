"""Decision maker extraction utilities."""

import logging
import re
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class DecisionMakerExtractor:
    """Extract key decision makers from company data."""
    
    # Common executive titles by role
    EXECUTIVE_TITLES = {
        'ceo': ['chief executive officer', 'ceo', 'founder', 'co-founder', 'owner', 'president', 'managing director'],
        'cto': ['chief technology officer', 'cto', 'tech lead', 'head of technology', 'vp of technology', 'director of technology'],
        'cfo': ['chief financial officer', 'cfo', 'finance director', 'head of finance', 'vp of finance', 'director of finance'],
        'coo': ['chief operating officer', 'coo', 'operations director', 'head of operations', 'vp of operations'],
        'vp_product': ['vp product', 'product director', 'head of product', 'chief product officer', 'director of product'],
        'vp_engineering': ['vp engineering', 'engineering director', 'head of engineering', 'director of engineering'],
        'vp_sales': ['vp sales', 'sales director', 'head of sales', 'chief revenue officer', 'cro', 'director of sales'],
        'vp_marketing': ['vp marketing', 'marketing director', 'head of marketing', 'cmo', 'chief marketing officer']
    }
    
    def extract_decision_makers(self, company_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract decision makers from company data
        
        Args:
            company_data: Dictionary containing company information
            
        Returns:
            List of dictionaries with decision maker information
        """
        decision_makers = []
        
        # Try to extract from people/employees field if available
        if 'people' in company_data:
            people = company_data.get('people', [])
            for person in people:
                if self._is_decision_maker(person.get('title', '')):
                    decision_makers.append({
                        'name': f"{person.get('first_name', '')} {person.get('last_name', '')}",
                        'title': person.get('title', ''),
                        'role': self._categorize_role(person.get('title', '')),
                        'source': 'company_api'
                    })
        
        # Try to extract from team/leadership field if available
        if 'team' in company_data:
            team = company_data.get('team', [])
            for member in team:
                if self._is_decision_maker(member.get('title', '')):
                    decision_makers.append({
                        'name': member.get('name', ''),
                        'title': member.get('title', ''),
                        'role': self._categorize_role(member.get('title', '')),
                        'source': 'company_api'
                    })
        
        # Extract from description as fallback
        if len(decision_makers) == 0 and 'description' in company_data:
            description_execs = self._extract_from_description(company_data.get('description', ''))
            decision_makers.extend(description_execs)
        
        # Add company info to each decision maker
        company_name = company_data.get('name', '')
        for dm in decision_makers:
            dm['company_name'] = company_name
            dm['company_id'] = company_data.get('id', '')
        
        return decision_makers
    
    def _is_decision_maker(self, title: Optional[str]) -> bool:
        """
        Check if title indicates a decision maker
        
        Args:
            title: Job title to check
            
        Returns:
            Boolean indicating if person is likely a decision maker
        """
        if not title:
            return False
            
        title = title.lower()
        
        # Check against known executive titles
        for role_titles in self.EXECUTIVE_TITLES.values():
            if any(role_title in title for role_title in role_titles):
                return True
        
        # Check for executive level indicators
        exec_indicators = ['chief', 'director', 'head', 'vp', 'vice president', 'president', 'founder']
        return any(indicator in title for indicator in exec_indicators)
    
    def _categorize_role(self, title: Optional[str]) -> str:
        """
        Categorize the executive role based on title
        
        Args:
            title: Job title to categorize
            
        Returns:
            Role category string
        """
        if not title:
            return 'unknown'
            
        title = title.lower()
        
        for role, role_titles in self.EXECUTIVE_TITLES.items():
            if any(role_title in title for role_title in role_titles):
                return role
        
        # Check for general executive indicators
        if any(term in title for term in ['chief', 'cxo']):
            return 'c_level'
        elif any(term in title for term in ['vp', 'vice president']):
            return 'vp_level'
        elif any(term in title for term in ['director', 'head']):
            return 'director_level'
        elif 'founder' in title:
            return 'founder'
            
        return 'other_executive'
    
    def _extract_from_description(self, description: str) -> List[Dict[str, Any]]:
        """
        Extract potential executives from company description
        
        Args:
            description: Company description text
            
        Returns:
            List of extracted decision makers
        """
        if not description:
            return []
        
        executives = []
        
        # Simple pattern matching for "Name, Title" or "Name (Title)" patterns
        # This is a basic implementation - could be improved with NLP
        patterns = [
            r'([A-Z][a-z]+ [A-Z][a-z]+)\s*,\s*([^,\.]+(?:founder|ceo|cto|chief|director|president)[^,\.]+)',
            r'([A-Z][a-z]+ [A-Z][a-z]+)\s*\(([^)]*(?:founder|ceo|cto|chief|director|president)[^)]*)\)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, description)
            for match in matches:
                name, title = match
                if self._is_decision_maker(title):
                    executives.append({
                        'name': name.strip(),
                        'title': title.strip(),
                        'role': self._categorize_role(title),
                        'source': 'company_description'
                    })
        
        return executives 