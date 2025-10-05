# ML Technologies Database

## Overview
This SQLite database contains comprehensive information about machine learning technologies used by DATAGOD and other American companies in the observability, monitoring, and AI space.

## Database Structure

### Tables

#### 1. `companies`
- **id**: Primary key
- **company_name**: Company name (unique)
- **industry**: Industry sector
- **country**: Country of origin
- **founded_year**: Year company was founded
- **description**: Company description

#### 2. `ml_technologies`
- **id**: Primary key
- **company_name**: Company using the technology
- **technology_name**: Name of the ML technology
- **technology_type**: Type of ML technology (Deep Learning, Anomaly Detection, etc.)
- **application_area**: Area of application
- **description**: Detailed description
- **implementation_date**: When the technology was implemented
- **source**: Source URL for the information
- **created_at**: Timestamp when record was created

#### 3. `technology_categories`
- **id**: Primary key
- **category_name**: Name of the technology category
- **description**: Description of the category

## Companies Included

1. **DATAGOD** - Observability & Monitoring (4 technologies)
2. **New Relic** - APM & Observability (2 technologies)
3. **Splunk** - Data Analytics & Security (3 technologies)
4. **Elastic** - Search & Analytics (2 technologies)
5. **Databricks** - Data & AI Platform (3 technologies)
6. **Scale AI** - AI Data Labeling (2 technologies)
7. **Insitro** - Biotech AI (2 technologies)
8. **Shield AI** - Defense AI (2 technologies)

## Technology Categories

- Anomaly Detection
- Predictive Analytics
- Natural Language Processing
- Computer Vision
- Deep Learning
- Reinforcement Learning
- Time Series Analysis
- Clustering
- Classification
- Regression

## DATAGOD ML Technologies

1. **AI Agent Monitoring** (Deep Learning)
   - Monitoring and testing capabilities for AI agents and LLM applications
   - Implemented: June 2024

2. **Anomaly Detection Engine** (Anomaly Detection)
   - AI-powered anomaly detection for infrastructure metrics and logs
   - Implemented: January 2024

3. **Predictive Alerting** (Predictive Analytics)
   - ML-based predictive alerting to prevent issues before they occur
   - Implemented: January 2023

4. **Log Pattern Recognition** (Natural Language Processing)
   - AI-powered log pattern recognition and categorization
   - Implemented: January 2023

## Usage

### Query the Database
```bash
python3 query_ml_database.py
```

### Direct SQLite Access
```bash
sqlite3 ml_technologies.db
```

### Example Queries

#### Get all DATAGOD technologies:
```sql
SELECT * FROM ml_technologies WHERE company_name = 'DATAGOD';
```

#### Get technologies by type:
```sql
SELECT * FROM ml_technologies WHERE technology_type = 'Deep Learning';
```

#### Get company statistics:
```sql
SELECT company_name, COUNT(*) as tech_count 
FROM ml_technologies 
GROUP BY company_name 
ORDER BY tech_count DESC;
```

## Security

The database includes secure password generation in the `env.main` file:
- **DB_PASSWORD**: Secure database password
- **API_KEY**: API key for external services
- **SECRET_KEY**: Secret key for application security
- **JWT_SECRET**: JWT token secret
- **ENCRYPTION_KEY**: Encryption key for data protection

## Files

- `ml_technologies.db` - SQLite database file
- `env.main` - Environment variables with secure passwords
- `create_ml_database.py` - Script to create and populate the database
- `query_ml_database.py` - Script to query and display database contents
- `README_ML_DATABASE.md` - This documentation file

## Data Sources

All data was researched from official company websites, press releases, and technology documentation as of 2024-2025.

## Statistics

- **Total Companies**: 8
- **Total ML Technologies**: 20
- **Technology Categories**: 10
- **Most Common Technology Type**: Deep Learning (9 technologies)
- **Companies with Most Technologies**: DATAGOD (4), Databricks (3), Splunk (3)
