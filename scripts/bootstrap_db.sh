#!/bin/bash
# Bootstrap database for AutoOutreach

set -e  # Exit on error

# Load environment variables
if [ -f "./configs/.env" ]; then
    echo "Loading environment variables from configs/.env"
    source ./configs/.env
else
    echo "Error: configs/.env file not found."
    echo "Please create it by copying configs/secrets.template.env"
    exit 1
fi

# Set defaults if not provided in env
DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}
DB_NAME=${DB_NAME:-autooutreach}
DB_USER=${DB_USER:-postgres}
DB_PASSWORD=${DB_PASSWORD:-password}

echo "Bootstrapping database $DB_NAME on $DB_HOST:$DB_PORT"

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "Error: PostgreSQL client (psql) not found."
    echo "Please install PostgreSQL first."
    exit 1
fi

# Create database if it doesn't exist
echo "Creating database $DB_NAME if it doesn't exist..."
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 || \
    PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -c "CREATE DATABASE $DB_NAME"

# Create tables
echo "Creating tables..."
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME << EOF
-- Companies table
CREATE TABLE IF NOT EXISTS companies (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    website VARCHAR(255),
    founded_date TIMESTAMP,
    headquarters VARCHAR(255),
    industries JSONB,
    funding_rounds JSONB,
    total_funding NUMERIC,
    employee_count INTEGER,
    crunchbase_id VARCHAR(64),
    sec_cik VARCHAR(64),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(64) NOT NULL
);

-- Contacts table
CREATE TABLE IF NOT EXISTS contacts (
    id VARCHAR(64) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    full_name VARCHAR(255),
    email VARCHAR(255),
    title VARCHAR(255),
    company_id VARCHAR(64) REFERENCES companies(id),
    company_name VARCHAR(255),
    linkedin_url VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(64) NOT NULL
);

-- Outreach table
CREATE TABLE IF NOT EXISTS outreach (
    id SERIAL PRIMARY KEY,
    contact_id VARCHAR(64) REFERENCES contacts(id),
    company_id VARCHAR(64) REFERENCES companies(id),
    status VARCHAR(32) NOT NULL,
    message_template VARCHAR(64),
    message_content TEXT,
    sent_at TIMESTAMP,
    response_received_at TIMESTAMP,
    response_content TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_companies_crunchbase_id ON companies(crunchbase_id);
CREATE INDEX IF NOT EXISTS idx_companies_sec_cik ON companies(sec_cik);
CREATE INDEX IF NOT EXISTS idx_contacts_company_id ON contacts(company_id);
CREATE INDEX IF NOT EXISTS idx_outreach_contact_id ON outreach(contact_id);
CREATE INDEX IF NOT EXISTS idx_outreach_company_id ON outreach(company_id);
CREATE INDEX IF NOT EXISTS idx_outreach_status ON outreach(status);
EOF

echo "Database bootstrap completed successfully!"
exit 0 