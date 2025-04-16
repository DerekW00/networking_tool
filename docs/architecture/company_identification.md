# Company & Decision-Maker Identification Pipeline

This document describes the pipeline for identifying target companies and their key decision makers.

## Pipeline Overview

```
┌─ Data Sources ─────┐   ┌─ Filtering ───────┐   ┌─ Extraction ──────┐   ┌─ Output ──────────┐
│                    │   │                   │   │                    │   │                   │
│  • Crunchbase API  │   │ • Location Filter │   │ • Decision Maker  │   │ • Raw Data (CSV)  │
│  • SEC EDGAR       ├──►│ • Funding Amount  ├──►│   Extraction      ├──►│ • Filtered Data   │
│  • (Future) News   │   │ • Industry Type   │   │ • Role            │   │ • Decision Makers │
│    APIs            │   │ • Funding Date    │   │   Categorization  │   │   (JSON)          │
│                    │   │                   │   │                    │   │                   │
└────────────────────┘   └───────────────────┘   └────────────────────┘   └───────────────────┘
```

## 1. Data Sources

The pipeline begins with the collection of company data from multiple sources:

### Crunchbase API
- Provides access to startup and funding information
- Daily CSV snapshot available in Community Edition
- Contains company details, funding rounds, and locations

### SEC EDGAR Database
- Public company filings (S-1, 10-K, 10-Q)
- Accessible via daily indices and file downloads
- Good source for established companies

### Future Potential Sources
- News APIs to track funding announcements
- AngelList/Pitchbook for earlier stage companies
- LinkedIn company pages for verification

## 2. Filtering

Raw company data is filtered to focus on target companies:

### Location Filtering
- Matches companies based on target locations in config
- Handles various formats of location data
- Supports case-insensitive and partial matching

### Funding Amount Filtering
- Focuses on companies with significant funding (configurable threshold)
- Helps prioritize companies with resources to purchase

### Other Filters
- Recent funding date (typically within last 12 months)
- Industry type (configurable in settings)
- Company size (employee count ranges)

## 3. Extraction

Once companies are filtered, the pipeline extracts key decision makers:

### Decision Maker Identification
- Analyzes job titles to identify key executives
- Categorizes by role (CEO, CTO, VP Engineering, etc.)
- Extracts from multiple data sources within company records

### Role Prioritization
- Prioritizes technical roles for technical products
- Focuses on business roles for business solutions
- Configurable via the decision_makers settings

### Name Normalization
- Handles various name formats and special characters
- Prepares names for the next enrichment stage

## 4. Output

The pipeline produces several outputs:

### Raw Data
- CSV files with all collected company data
- Stored in data/raw/ directory
- Useful for auditing and debugging

### Filtered Companies
- CSV files with companies that passed all filters
- Stored in data/interim/ directory
- Input for the enrichment stage

### Companies with Decision Makers
- JSON file mapping companies to their key executives
- Includes role categorization
- Primary input for the enricher module

## Configuration

The pipeline is configured via YAML files:

```yaml
# Target locations
target_locations:
  - "San Francisco"
  - "New York"
  # ...more locations

# Filtering settings
filtering:
  min_funding_amount: 500000  # $500k minimum
  max_funding_age_days: 365   # Funded within last year
  target_industries:
    - "software"
    - "fintech"
    # ...more industries

# Decision maker settings
decision_makers:
  priority_roles:
    - "cto"
    - "vp_engineering"
    # ...more roles
  min_decision_makers_per_company: 1
```

## Next Steps

The output of this pipeline feeds into the Enricher module, which:

1. Looks up additional details about identified executives
2. Finds contact information and social profiles
3. Prepares data for the Outreach Bot's LinkedIn automation 