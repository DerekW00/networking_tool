"""Common type definitions for AutoOutreach."""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Union

from pydantic import BaseModel, Field


class FundingRound(str, Enum):
    """Enumeration of funding round types."""
    
    SEED = "seed"
    ANGEL = "angel"
    SERIES_A = "series_a"
    SERIES_B = "series_b"
    SERIES_C = "series_c"
    SERIES_D = "series_d"
    SERIES_E = "series_e"
    SERIES_F = "series_f"
    GROWTH = "growth"
    IPO = "ipo"
    DEBT = "debt"
    GRANT = "grant"
    OTHER = "other"


class Industry(str, Enum):
    """Enumeration of industry sectors."""
    
    TECHNOLOGY = "technology"
    HEALTHCARE = "healthcare"
    FINANCE = "finance"
    EDUCATION = "education"
    RETAIL = "retail"
    MANUFACTURING = "manufacturing"
    MEDIA = "media"
    AUTOMOTIVE = "automotive"
    REAL_ESTATE = "real_estate"
    ENERGY = "energy"
    TRANSPORTATION = "transportation"
    AGRICULTURE = "agriculture"
    OTHER = "other"


class Funding(BaseModel):
    """Model representing a funding round."""
    
    amount: Optional[float] = None
    currency: str = "USD"
    announced_date: Optional[datetime] = None
    round_type: FundingRound = FundingRound.OTHER
    investors: List[str] = Field(default_factory=list)
    lead_investor: Optional[str] = None
    post_money_valuation: Optional[float] = None


class Company(BaseModel):
    """Model representing a company."""
    
    id: str
    name: str
    description: Optional[str] = None
    website: Optional[str] = None
    founded_date: Optional[datetime] = None
    headquarters: Optional[str] = None
    industries: List[Industry] = Field(default_factory=list)
    funding_rounds: List[Funding] = Field(default_factory=list)
    total_funding: Optional[float] = None
    employee_count: Optional[int] = None
    
    # External IDs
    crunchbase_id: Optional[str] = None
    sec_cik: Optional[str] = None
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    source: str = "unknown"


class Contact(BaseModel):
    """Model representing a contact person."""
    
    id: str
    first_name: str
    last_name: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    title: Optional[str] = None
    company_id: Optional[str] = None
    company_name: Optional[str] = None
    linkedin_url: Optional[str] = None
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    source: str = "unknown" 