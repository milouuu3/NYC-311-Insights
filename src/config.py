"""
Configuration file for NYC 311 Insights project.
Centralized settings for data collection and processing.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ============================================
# API CREDENTIALS
# ============================================
NYC_APP_TOKEN = os.getenv("NYC_APP_TOKEN")

# ============================================
# DATE RANGE
# ============================================
START_DATE = "2023-01-01"
END_DATE = "2024-12-31"

# ============================================
# NYC 311 DATA SETTINGS
# ============================================
NYC_311_DATASET_ID = "erm2-nwe9"
NYC_311_BATCH_SIZE = 30  # Days per batch
NYC_311_TIMEOUT = 60  # API timeout in seconds
NYC_311_REQUEST_LIMIT = 50000  # Records per API request
NYC_311_OUTPUT_DIR = "data/raw/311"

# Columns to fetch from 311 API
NYC_311_COLUMNS = [
    "unique_key",
    "created_date",
    "closed_date",
    "agency",
    "complaint_type",
    "descriptor",
    "status",
    "borough",
    "latitude",
    "longitude",
]

# ============================================
# WEATHER DATA SETTINGS
# ============================================
# NYC coordinates (Manhattan center)
NYC_LATITUDE = 40.7128
NYC_LONGITUDE = -74.0060
NYC_TIMEZONE = "America/New_York"

WEATHER_OUTPUT_DIR = "data/raw/weather"

# Weather variables to fetch (daily aggregates)
WEATHER_VARIABLES = [
    "temperature_2m_mean",
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "rain_sum",
    "snowfall_sum",
    "windspeed_10m_max",
    "weathercode",
]

# ============================================
# PATHS
# ============================================
DATA_RAW_DIR = "data/raw"
DATA_PROCESSED_DIR = "data/processed"
MODELS_DIR = "models"
NOTEBOOKS_DIR = "notebooks"
