#!/usr/bin/env python
"""
Demo script to demonstrate the company & decision maker identification pipeline.
This script uses sample data to show how the pipeline works without making actual API calls.
"""

import json
import logging
import os
import sys
from pathlib import Path

import pandas as pd

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from apps.collector.src.collector.filters import LocationFilter
from apps.collector.src.collector.extractors import DecisionMakerExtractor
from apps.collector.src.collector.storage import save_to_json


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("demo")


def load_sample_data():
    """Load sample company data for demonstration."""
    # Create a directory for sample data if it doesn't exist
    sample_dir = Path(__file__).parent / "sample_data"
    sample_dir.mkdir(exist_ok=True)
    
    # Sample company data
    companies = [
        {
            "id": "company1",
            "name": "TechInnovate AI",
            "description": "AI-powered analytics platform for enterprise customers. Founded by Sarah Chen, CEO and Michael Johnson, CTO.",
            "headquarters": "San Francisco, CA",
            "funding_rounds": [
                {"amount": 5000000, "date": "2023-05-15", "stage": "Series A"}
            ],
            "people": [
                {"first_name": "Sarah", "last_name": "Chen", "title": "CEO"},
                {"first_name": "Michael", "last_name": "Johnson", "title": "CTO"},
                {"first_name": "David", "last_name": "Singh", "title": "Software Engineer"}
            ]
        },
        {
            "id": "company2",
            "name": "DataFlow Systems",
            "description": "Enterprise data integration platform for high-volume transactions.",
            "headquarters": "New York, NY",
            "funding_rounds": [
                {"amount": 8000000, "date": "2023-06-22", "stage": "Series B"}
            ],
            "team": [
                {"name": "Robert Garcia", "title": "Founder & CEO"},
                {"name": "Jennifer Adams", "title": "VP of Engineering"},
                {"name": "Thomas Lee", "title": "Product Manager"}
            ]
        },
        {
            "id": "company3",
            "name": "CloudSecurity Pro",
            "description": "Cloud security solutions for midsize businesses.",
            "headquarters": "Chicago, IL",
            "funding_rounds": [
                {"amount": 3000000, "date": "2023-04-10", "stage": "Seed"}
            ],
            "people": [
                {"first_name": "James", "last_name": "Wilson", "title": "Founder"},
                {"first_name": "Lisa", "last_name": "Brown", "title": "Head of Sales"},
                {"first_name": "Kevin", "last_name": "Martin", "title": "Lead Developer"}
            ]
        },
        {
            "id": "company4",
            "name": "MedTech Solutions",
            "description": "Medical device startup focused on remote patient monitoring.",
            "headquarters": "Boston, MA",
            "funding_rounds": [
                {"amount": 12000000, "date": "2023-03-05", "stage": "Series A"}
            ],
            "people": [
                {"first_name": "Emily", "last_name": "Taylor", "title": "CEO"},
                {"first_name": "Dr. Richard", "last_name": "Wong", "title": "Chief Medical Officer"},
                {"first_name": "Amanda", "last_name": "Peters", "title": "CTO"}
            ]
        },
        {
            "id": "company5",
            "name": "GreenEnergy Systems",
            "description": "Renewable energy solutions for commercial buildings.",
            "headquarters": "Portland, OR",
            "funding_rounds": [
                {"amount": 7500000, "date": "2023-07-18", "stage": "Series A"}
            ],
            "team": [
                {"name": "Daniel Green", "title": "CEO & Co-founder"},
                {"name": "Sophia Martinez", "title": "COO"},
                {"name": "Nathan Lewis", "title": "Head of R&D"}
            ]
        }
    ]
    
    # Save and load as DataFrame to simulate how we'd process real data
    sample_file = sample_dir / "sample_companies.json"
    with open(sample_file, "w") as f:
        json.dump(companies, f, indent=2)
    
    logger.info(f"Created sample data with {len(companies)} companies")
    return pd.DataFrame(companies)


def demo_pipeline():
    """Run the company & decision maker identification pipeline with sample data."""
    logger.info("Starting company & decision maker identification demo")
    
    # 1. Load sample data
    logger.info("Loading sample company data")
    df_companies = load_sample_data()
    
    # 2. Configure location filter
    target_locations = ["San Francisco", "New York", "Boston"]
    logger.info(f"Filtering companies by locations: {', '.join(target_locations)}")
    location_filter = LocationFilter(target_locations)
    
    # 3. Filter companies by location
    df_filtered = df_companies[
        df_companies["headquarters"].apply(lambda loc: location_filter.is_in_target_location(loc))
    ]
    logger.info(f"Filtered {len(df_companies)} companies down to {len(df_filtered)} based on location")
    
    # 4. Extract decision makers
    extractor = DecisionMakerExtractor()
    companies_with_decision_makers = []
    
    for _, company in df_filtered.iterrows():
        company_dict = company.to_dict()
        decision_makers = extractor.extract_decision_makers(company_dict)
        
        if decision_makers:
            companies_with_decision_makers.append({
                "company": {
                    "id": company_dict["id"],
                    "name": company_dict["name"],
                    "description": company_dict.get("description", ""),
                    "headquarters": company_dict["headquarters"],
                    "funding_rounds": company_dict.get("funding_rounds", [])
                },
                "decision_makers": decision_makers
            })
    
    logger.info(f"Found {len(companies_with_decision_makers)} companies with decision makers")
    
    # 5. Save results
    output_dir = Path(__file__).parent / "sample_data"
    output_file = output_dir / "companies_with_decision_makers.json"
    save_to_json(companies_with_decision_makers, output_file)
    
    # 6. Display results
    logger.info("\n--- DEMO RESULTS ---")
    logger.info(f"Target Locations: {', '.join(target_locations)}")
    logger.info(f"Total Companies: {len(df_companies)}")
    logger.info(f"Filtered Companies: {len(df_filtered)}")
    logger.info(f"Companies with Decision Makers: {len(companies_with_decision_makers)}\n")
    
    for company_data in companies_with_decision_makers:
        company = company_data["company"]
        decision_makers = company_data["decision_makers"]
        
        logger.info(f"Company: {company['name']} (Location: {company['headquarters']})")
        logger.info("Decision Makers:")
        for dm in decision_makers:
            logger.info(f"  - {dm['name']} ({dm['title']}) - Role: {dm['role']}")
        logger.info("")
    
    logger.info(f"Results saved to {output_file}")


if __name__ == "__main__":
    demo_pipeline() 