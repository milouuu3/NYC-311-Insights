# NYC 311 Service Request Insights

Data pipeline for analyzing and predicting NYC 311 service request patterns using historical complaint data combined with weather information.

## Overview

This project analyzes NYC 311 service requests to identify patterns and correlations with weather conditions. The goal is to predict service request volumes and types based on historical data and weather patterns.

## Data Sources

- **NYC 311 Service Requests**: [NYC Open Data Portal](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9/about_data)
- **Weather Data**: [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api)

## Project Structure

```
nyc-311-insights/
├── data/
│   ├── raw/
│   │   ├── 311/          # Raw 311 service request data
│   │   └── weather/      # Raw weather data
│   └── processed/        # Cleaned and processed data
├── src/
│   ├── fetch_311_data.py      # Script to fetch 311 data
│   ├── fetch_weather_data.py  # Script to fetch weather data
│   ├── test_nyc.py           # Test NYC 311 API connection
│   └── test_meteo.py         # Test weather API connection
├── notebooks/            # Jupyter notebooks for analysis
├── models/              # Trained models
├── .env                 # Environment variables (API keys)
└── requirements.txt     # Python dependencies

```

## Data Fields

### 311 Service Requests
- `unique_key`: Unique identifier for each request
- `created_date`: When the request was created
- `closed_date`: When the request was closed
- `complaint_type`: Type of complaint
- `descriptor`: Additional complaint details
- `borough`: NYC borough
- `latitude`, `longitude`: Location coordinates
- `agency`: Responding agency
- `status`: Request status

### Weather Data
- Temperature
- Precipitation
- Snow
- Wind speed
- Weather conditions
