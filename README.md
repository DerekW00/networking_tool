# AutoOutreach

A modular system for identifying and reaching out to companies based on funding data.

## Overview

AutoOutreach is a collection of micro-apps designed to automate the outreach process:

1. **Collector** - Fetches funding and company data from sources like Crunchbase and SEC filings
2. **Enricher** - Looks up executive contacts using services like Clearbit and People Data Labs
3. **Outreach Bot** - Automates LinkedIn outreach using Playwright
4. **WebUI** - Optional Next.js dashboard for monitoring and configuration

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

### Collector

```bash
cd apps/collector
python -m collector --config ../../configs/dev/collector.yaml
```

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

