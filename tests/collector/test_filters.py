"""Tests for the location filter module."""

import pytest
from collector.filters import LocationFilter


def test_location_filter_initialization():
    """Test initializing the LocationFilter with target locations."""
    target_locations = ["San Francisco", "New York", "London"]
    filter = LocationFilter(target_locations)
    
    assert filter.target_locations == ["san francisco", "new york", "london"]
    assert filter.location_cache == {}


def test_is_in_target_location_exact_match():
    """Test exact location matches."""
    target_locations = ["San Francisco", "New York", "London"]
    filter = LocationFilter(target_locations)
    
    assert filter.is_in_target_location("San Francisco")
    assert filter.is_in_target_location("New York")
    assert filter.is_in_target_location("London")


def test_is_in_target_location_case_insensitive():
    """Test case-insensitive location matching."""
    target_locations = ["San Francisco", "New York", "London"]
    filter = LocationFilter(target_locations)
    
    assert filter.is_in_target_location("san francisco")
    assert filter.is_in_target_location("NEW YORK")
    assert filter.is_in_target_location("london")


def test_is_in_target_location_partial_match():
    """Test partial location matches."""
    target_locations = ["San Francisco", "New York", "London"]
    filter = LocationFilter(target_locations)
    
    assert filter.is_in_target_location("San Francisco, CA")
    assert filter.is_in_target_location("Downtown New York")
    assert filter.is_in_target_location("London, UK")


def test_is_in_target_location_no_match():
    """Test non-matching locations."""
    target_locations = ["San Francisco", "New York", "London"]
    filter = LocationFilter(target_locations)
    
    assert not filter.is_in_target_location("Los Angeles")
    assert not filter.is_in_target_location("Chicago")
    assert not filter.is_in_target_location("Paris")


def test_is_in_target_location_none_or_empty():
    """Test handling of None or empty location strings."""
    target_locations = ["San Francisco", "New York", "London"]
    filter = LocationFilter(target_locations)
    
    assert not filter.is_in_target_location(None)
    assert not filter.is_in_target_location("")


def test_filter_companies():
    """Test filtering a list of companies."""
    target_locations = ["San Francisco", "New York", "London"]
    filter = LocationFilter(target_locations)
    
    companies = [
        {"name": "Company A", "headquarters": "San Francisco"},
        {"name": "Company B", "headquarters": "Los Angeles"},
        {"name": "Company C", "headquarters": "New York, NY"},
        {"name": "Company D", "headquarters": "London, UK"},
        {"name": "Company E", "headquarters": None},
    ]
    
    filtered = filter.filter_companies(companies)
    
    assert len(filtered) == 3
    assert filtered[0]["name"] == "Company A"
    assert filtered[1]["name"] == "Company C"
    assert filtered[2]["name"] == "Company D"
    
    # Test with different location field name
    companies = [
        {"name": "Company A", "location": "San Francisco"},
        {"name": "Company B", "location": "Los Angeles"},
    ]
    
    filtered = filter.filter_companies(companies, location_field="location")
    
    assert len(filtered) == 1
    assert filtered[0]["name"] == "Company A" 