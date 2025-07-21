# HealthKart Influencer Campaign Dashboard

## Overview
This Streamlit dashboard allows HealthKart to track, analyze, and report the performance of influencer marketing campaigns.

## Features
- Campaign and Influencer Tracking
- Incremental ROAS Calculation
- Influencer Insights and Payout Analysis
- Filtering by brand, platform, influencer type
- Export to CSV/PDF (optional)

## Setup
```bash
pip install -r requirements.txt
streamlit run app/main.py
```

## Assumptions
- All datasets are simulated.
- ROAS = Revenue / Payout (for influencers with 'order'-based payments).

## Files
- `data/` - All input datasets
- `app/` - Main Streamlit application code
- `insights/` - Summary PDF with insights

