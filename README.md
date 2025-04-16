# AutoOutreach

A modular system for identifying and reaching out to companies based on funding data.

## Overview

AutoOutreach is a collection of micro-apps designed to automate the outreach process:

1. **Collector** - Fetches funding and company data from sources like Crunchbase and SEC filings
2. **Enricher** - Looks up executive contacts using services like Clearbit and People Data Labs
3. **Outreach Bot** - Automates LinkedIn outreach using Playwright
4. **WebUI** - Optional Next.js dashboard for monitoring and configuration

## Key Features

- **Targeted Company Identification**: Automatically discover recently funded startups in specific geographic locations
- **Decision Maker Extraction**: Identify key executives like CEOs, CTOs, and VPs based on their roles
- **Contact Enrichment**: Find email addresses and social profiles for decision makers
- **Automated Outreach**: Send personalized connection requests and follow-up messages on LinkedIn
- **Performance Tracking**: Monitor campaign results and optimize your approach

## Pipeline Architecture

```
┌───────────┐    ┌───────────┐    ┌───────────┐    ┌───────────┐
│           │    │           │    │           │    │           │
│ Collector ├───►│ Enricher  ├───►│ Outreach  │◄───┤  WebUI    │
│           │    │           │    │   Bot     │    │           │
└─────┬─────┘    └─────┬─────┘    └─────┬─────┘    └─────┬─────┘
      │                │                │                │
      ▼                ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                        Database                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Project Structure

```
AutoOutreach/
│
├─ apps/                    # runnable micro‑apps
│   ├─ collector/           # funding & company fetcher
│   ├─ enricher/            # exec‑lookup (Clearbit/PDL)
│   ├─ outreach_bot/        # Playwright LinkedIn agent
│   └─ webui/               # optional Next.js dashboard
│
├─ libs/                    # shared, importable packages
│   ├─ common/              # typing, logging, retry helpers
│   └─ geo_utils/
│
├─ configs/                 # YAML/TOML env‑specific settings
├─ data/                    # raw & processed artifacts
├─ tests/                   # pytest suites
├─ scripts/                 # one‑off CLI helpers
├─ docs/                    # MkDocs site
├─ docker/                  # Dockerfiles per micro‑app
```

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+ (for WebUI)
- Docker (optional)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/autooutreach.git
   cd autooutreach
   ```

2. Set up virtual environments:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   # For collector
   cd apps/collector
   pip install -e .
   
   # For common libs
   cd ../../libs/common
   pip install -e .
   ```

4. Set up configuration:
   ```
   cp configs/secrets.template.env configs/.env
   # Edit configs/.env with your API keys
   ```

## Usage

### Collector: Finding Companies & Decision Makers

The Collector module identifies recently funded companies and their key decision makers:

```bash
# Run with default settings
python -m collector

# Filter by specific locations
python -m collector --target-locations "San Francisco" "New York" "London"

# Set a custom date range
python -m collector --start-date 2023-01-01 --end-date 2023-03-31
```

The collector will:
1. Fetch data from Crunchbase and SEC filings
2. Filter companies by your target locations
3. Extract key decision makers (founders, C-level, VPs)
4. Save both raw and processed data for enrichment

### Enricher

```bash
cd apps/enricher
python -m enricher --config ../../configs/dev/enricher.yaml
```

### Outreach Bot

```bash
cd apps/outreach_bot
python -m outreach_bot --config ../../configs/dev/outreach_bot.yaml
```

## Documentation

For more detailed documentation, see the [docs](docs/) directory or run:

```bash
pip install mkdocs
mkdocs serve
```

Then visit http://localhost:8000 in your browser.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 

