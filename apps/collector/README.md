# Collector

The Collector app is responsible for fetching funding and company data from various sources.

## Features

- Fetches company data from Crunchbase, SEC, and other sources
- Processes and standardizes data formats
- Stores results for further enrichment

## Usage

```bash
# Run the collector with default settings
python -m collector

# Run with a specific config
python -m collector --config ../../configs/dev/collector.yaml

# Fetch data for a specific timeframe
python -m collector --start-date 2023-01-01 --end-date 2023-01-31
```

## Configuration

See `configs/dev/collector.yaml` and `configs/prod/collector.yaml` for configuration options. 