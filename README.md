# Daily Search KPI Automation

Automated reporting pipeline that extracts search analytics data from Redshift,
computes KPIs using Pandas, and sends automated HTML email reports.

## Features

- Redshift data extraction
- Automated KPI calculation
- Data freshness validation
- HTML email reporting
- Email audit logging
- Failure alerting system

## Tech Stack

Python  
Pandas  
Redshift (PostgreSQL)  
SMTP Email Automation  

## Project Structure

daily_search_kpi/
│
├── src/
│   ├── main.py
│   ├── db.py
│   ├── emailer.py
│   └── kpi_calc.py
│
├── sql/
│   └── base_query.sql
│
├── config/
│   ├── redshift_creds_template.json
│   └── email_creds_template.json
│
├── logs/
├── requirements.txt
└── README.md

## Run Locally
