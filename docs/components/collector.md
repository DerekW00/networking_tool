# Collector Component

The Collector is responsible for gathering company and funding data from various sources, filtering it based on target locations, and identifying key decision makers within these companies.

## Overview

The Collector module follows a pipeline architecture:

1. **Data Collection**: Fetches company and funding data from Crunchbase and SEC filings
2. **Location Filtering**: Narrows down companies to target geographic regions
3. **Decision Maker Extraction**: Identifies key executives in each company
4. **Data Storage**: Saves both raw and processed data for further enrichment

## Configuration

The collector is configured via YAML files in the `configs/` directory:

```yaml
# Target locations for filtering
target_locations:
  - "San Francisco"
  - "New York"
  - "Boston"
  # Additional locations...

# Collection parameters
collection:
  max_days_per_run: 30
  rate_limit_delay: 1.0
  min_funding_amount: 500000

# Decision maker extraction settings
decision_makers:
  min_roles_per_company: 1
  target_roles:
    - "ceo"
    - "cto"
    - "founder"
    # Additional roles...
```

## Data Sources

### Crunchbase

The collector fetches data from Crunchbase using their API, specifically looking for:
- Recently funded companies
- Company details including name, location, description
- Funding information (amount, date, investors)

### SEC EDGAR Database

For public companies, the collector fetches data from SEC filings, focusing on:
- S-1 filings (Initial public offerings)
- 10-K and 10-Q reports (Annual and quarterly filings)

## Location Filtering

Companies are filtered based on the target locations specified in the configuration. The `LocationFilter` class handles:

- Case-insensitive matching
- Partial location matching
- Handling of multiple office locations

## Decision Maker Extraction

The `DecisionMakerExtractor` identifies key executives in companies based on:

1. Job title analysis (CEO, CTO, VP of Engineering, etc.)
2. Role categorization for easier targeting
3. Fallback extraction from company descriptions when executive data is limited

## Usage

To run the collector with default settings:

```bash
python -m collector
```

With specific config:

```bash
python -m collector --config ../../configs/dev/collector.yaml
```

With command line overrides:

```bash
python -m collector --start-date 2023-01-01 --end-date 2023-01-31 --target-locations "San Francisco" "New York"
```

## Output

The collector produces several outputs:

1. **Raw Data**: Unfiltered data from all sources in `data/raw/`
2. **Filtered Companies**: Companies matching target locations in `data/interim/`
3. **Companies with Decision Makers**: A JSON file containing companies and their key executives in `data/interim/companies_with_decision_makers.json`

## Next Steps

The output of the Collector module is designed to feed into the Enricher module, which will:

1. Lookup additional information about companies and decision makers
2. Find contact details for identified executives
3. Prepare data for the Outreach Bot 