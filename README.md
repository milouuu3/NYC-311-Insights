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

## Analysis Pipeline

### Notebooks

1. **01_explore_311_data.ipynb** - Exploratory analysis of 311 data
   - 6.9M service requests across 2 years (2023-2024)
   - Top complaint types, borough distribution, temporal patterns
   - 21% of complaints are weather-related

2. **02_explore_weather_data.ipynb** - Weather data exploration
   - 731 days of daily weather data
   - Temperature, precipitation, wind speed analysis
   - Seasonal patterns and trends

3. **03_combine_311_weather.ipynb** - Merging datasets
   - Daily aggregation of 311 complaints
   - Correlation analysis between weather and complaints
   - Finding: Very weak correlation (-0.097) between temperature and total complaints

4. **04_feature_engineering.ipynb** - Feature creation
   - 57 engineered features including:
     - Complaint type breakdowns (top 15 types)
     - Borough-level aggregations
     - Time features (day of week, month, season, weekend flags)
     - Weather categories (is_rainy, is_hot, temperature bins)
     - Lag features (previous day weather, 7-day rolling averages)

5. **05_modeling.ipynb** - Predictive modeling
   - Models tested: Linear Regression, Ridge, Lasso, Random Forest, Gradient Boosting
   - Best model: Ridge Regression (Test R² = -0.048, RMSE = 2329)
   - **Key Finding**: Weather features alone are insufficient for predicting total complaint volume

## Key Findings

- **Weather has minimal predictive power for total 311 complaints** (all models achieved negative R² scores)
- Total complaints aggregate many types with opposing weather relationships (e.g., heat complaints ↑ when cold, noise complaints ↑ when hot)
- Ridge/Lasso regularization performed best by preventing overfitting on weak signals
- Tree-based models (Random Forest, Gradient Boosting) showed severe overfitting (train R² ~0.85, test R² ~-0.10)

## Recommendations

Future work should focus on:
1. Predicting **specific complaint types** rather than total volume (e.g., HEAT/HOT WATER vs temperature)
2. Adding non-weather features (holidays, events, school schedules)
3. Using time series models to capture temporal autocorrelation

## Data

### 311 Service Requests
- `unique_key`: Unique identifier for each request
- `created_date`: When the request was created
- `closed_date`: When the request was closed
- `complaint_type`: Type of complaint (e.g., Illegal Parking, Noise, HEAT/HOT WATER)
- `descriptor`: Additional complaint details
- `borough`: NYC borough (Bronx, Brooklyn, Manhattan, Queens, Staten Island)
- `latitude`, `longitude`: Location coordinates
- `agency`: Responding agency
- `status`: Request status

### Weather Data
- `temperature_2m_mean/max/min`: Daily temperature (°C)
- `precipitation_sum`: Total daily precipitation (mm)
- `rain_sum`: Daily rainfall (mm)
- `snowfall_sum`: Daily snowfall (cm)
- `windspeed_10m_max`: Maximum wind speed (km/h)
- `weathercode`: WMO weather condition code
