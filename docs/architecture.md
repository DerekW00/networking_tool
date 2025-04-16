# AutoOutreach Architecture

This document describes the high-level architecture of the AutoOutreach system.

## System Overview

AutoOutreach is designed as a collection of loosely-coupled micro-apps that work together to automate the process of identifying and reaching out to companies based on funding data.

The system follows a pipeline architecture, where data flows through several stages:

1. **Collection**: Gathering company and funding data from external sources
2. **Enrichment**: Adding contact information for key executives
3. **Outreach**: Automating personalized outreach via LinkedIn
4. **Monitoring**: Tracking campaign performance via a web dashboard

## Component Diagram

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

## Data Flow

1. The **Collector** app fetches company and funding data from sources like Crunchbase and SEC filings, storing raw data in the `data/raw/` directory and processed entries in the database.

2. The **Enricher** app retrieves companies from the database, looks up executive contact information using services like Clearbit and People Data Labs, and updates the database with contact details.

3. The **Outreach Bot** retrieves contacts from the database, uses templates to generate personalized messages, and sends connection requests and messages via LinkedIn using Playwright for browser automation.

4. The **WebUI** provides a dashboard for configuring, monitoring, and analyzing outreach campaigns.

## Technology Stack

- **Backend**: Python 3.9+ for data processing and automation
- **Frontend**: Next.js for the web dashboard
- **Database**: PostgreSQL for structured data storage
- **Storage**: File system for raw data artifacts
- **Configuration**: YAML files for environment-specific settings
- **Deployment**: Docker containers for each micro-app

## Security Considerations

- API keys and credentials are stored as environment variables, not in the codebase
- Sensitive data is encrypted in the database
- Rate limiting is implemented for all external API calls
- The outreach bot respects LinkedIn's terms of service and implements ethical limits

## Development Workflow

1. Changes are developed in feature branches
2. CI runs tests and linting on pull requests
3. Merged changes trigger automated deployments
4. Deployment is done using Docker Compose or Kubernetes 