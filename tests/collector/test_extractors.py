"""Tests for the decision maker extractor module."""

import pytest
from collector.extractors import DecisionMakerExtractor


def test_decision_maker_extractor_initialization():
    """Test initializing the DecisionMakerExtractor."""
    extractor = DecisionMakerExtractor()
    assert hasattr(extractor, 'EXECUTIVE_TITLES')
    assert isinstance(extractor.EXECUTIVE_TITLES, dict)


def test_is_decision_maker():
    """Test identifying decision makers by title."""
    extractor = DecisionMakerExtractor()
    
    # Test positive cases
    assert extractor._is_decision_maker("CEO")
    assert extractor._is_decision_maker("Chief Executive Officer")
    assert extractor._is_decision_maker("Founder")
    assert extractor._is_decision_maker("Co-founder & CTO")
    assert extractor._is_decision_maker("VP of Engineering")
    assert extractor._is_decision_maker("Director of Product")
    assert extractor._is_decision_maker("Head of Sales")
    
    # Test negative cases
    assert not extractor._is_decision_maker("Software Engineer")
    assert not extractor._is_decision_maker("Marketing Specialist")
    assert not extractor._is_decision_maker("Customer Support")
    assert not extractor._is_decision_maker(None)
    assert not extractor._is_decision_maker("")


def test_categorize_role():
    """Test categorizing roles based on title."""
    extractor = DecisionMakerExtractor()
    
    assert extractor._categorize_role("CEO") == "ceo"
    assert extractor._categorize_role("Chief Executive Officer") == "ceo"
    assert extractor._categorize_role("Founder & CEO") == "ceo"
    
    assert extractor._categorize_role("CTO") == "cto"
    assert extractor._categorize_role("Chief Technology Officer") == "cto"
    assert extractor._categorize_role("VP of Technology") == "cto"
    
    assert extractor._categorize_role("VP of Engineering") == "vp_engineering"
    assert extractor._categorize_role("Engineering Director") == "vp_engineering"
    
    assert extractor._categorize_role("CFO") == "cfo"
    assert extractor._categorize_role("Chief Product Officer") == "vp_product"
    
    # Test general categories
    assert extractor._categorize_role("Chief Revenue Officer") == "vp_sales"
    assert extractor._categorize_role("Chief Something Officer") == "c_level"
    assert extractor._categorize_role("VP of Something") == "vp_level"
    assert extractor._categorize_role("Director of Something") == "director_level"
    
    assert extractor._categorize_role(None) == "unknown"


def test_extract_from_description():
    """Test extracting decision makers from company descriptions."""
    extractor = DecisionMakerExtractor()
    
    # Test simple cases
    description = "Founded in 2020 by John Smith, CEO and Jane Doe, CTO."
    executives = extractor._extract_from_description(description)
    assert len(executives) > 0
    
    # Test with different formats
    description = "Our leadership team includes John Smith (Founder & CEO) and Jane Doe (CTO)."
    executives = extractor._extract_from_description(description)
    assert len(executives) > 0
    
    # Test with no executives mentioned
    description = "Our company was founded in 2020 and specializes in AI solutions."
    executives = extractor._extract_from_description(description)
    assert len(executives) == 0
    
    # Test with None
    executives = extractor._extract_from_description(None)
    assert len(executives) == 0


def test_extract_decision_makers():
    """Test extracting decision makers from company data."""
    extractor = DecisionMakerExtractor()
    
    # Test with people array
    company_data = {
        "id": "company123",
        "name": "Test Company",
        "people": [
            {"first_name": "John", "last_name": "Smith", "title": "CEO"},
            {"first_name": "Jane", "last_name": "Doe", "title": "CTO"},
            {"first_name": "Bob", "last_name": "Johnson", "title": "Software Engineer"}
        ]
    }
    
    executives = extractor.extract_decision_makers(company_data)
    assert len(executives) == 2
    assert executives[0]["name"] == "John Smith"
    assert executives[0]["role"] == "ceo"
    assert executives[0]["company_name"] == "Test Company"
    assert executives[1]["name"] == "Jane Doe"
    assert executives[1]["role"] == "cto"
    
    # Test with team array
    company_data = {
        "id": "company456",
        "name": "Another Company",
        "team": [
            {"name": "John Smith", "title": "Founder & CEO"},
            {"name": "Jane Doe", "title": "Head of Engineering"},
            {"name": "Bob Johnson", "title": "Developer"}
        ]
    }
    
    executives = extractor.extract_decision_makers(company_data)
    assert len(executives) == 2
    assert executives[0]["name"] == "John Smith"
    assert executives[0]["role"] == "ceo"
    assert executives[1]["name"] == "Jane Doe"
    assert executives[1]["role"] == "vp_engineering"
    
    # Test fallback to description
    company_data = {
        "id": "company789",
        "name": "Third Company",
        "description": "Founded by John Smith (CEO) and Jane Doe (CTO) in 2020."
    }
    
    executives = extractor.extract_decision_makers(company_data)
    assert len(executives) > 0
    
    # Test with no usable data
    company_data = {
        "id": "company000",
        "name": "Empty Company"
    }
    
    executives = extractor.extract_decision_makers(company_data)
    assert len(executives) == 0 