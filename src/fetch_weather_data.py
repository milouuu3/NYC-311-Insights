import os
import pandas as pd
import openmeteo_requests
import requests_cache
from retry_requests import retry
from config import (
    START_DATE,
    END_DATE,
    NYC_LATITUDE,
    NYC_LONGITUDE,
    NYC_TIMEZONE,
    WEATHER_OUTPUT_DIR,
    WEATHER_VARIABLES
)


def fetch_data(start_date, end_date):
    """Fetch daily weather data from Open-Meteo API."""
    # Setup the Open-Meteo API client with cache and retry
    cache_session = requests_cache.CachedSession(".cache", expire_after=-1)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": NYC_LATITUDE,
        "longitude": NYC_LONGITUDE,
        "start_date": start_date,
        "end_date": end_date,
        "daily": WEATHER_VARIABLES,
        "timezone": NYC_TIMEZONE,
    }

    print(f"Fetching weather data from {start_date} to {end_date}...")
    print(f"Location: {NYC_LATITUDE}°N, {NYC_LONGITUDE}°W (NYC)")

    try:
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]

        print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Elevation: {response.Elevation()} m asl")
        print(f"Timezone: {response.Timezone()}")

        return response
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None


def process_data(response):
    """Process weather API response into a DataFrame."""
    daily = response.Daily()

    # Create date range
    date_range = pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s", utc=True),
        end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left",
    )

    # Build data dictionary
    data = {"date": date_range}

    # Add each weather variable
    for i, var in enumerate(WEATHER_VARIABLES):
        data[var] = daily.Variables(i).ValuesAsNumpy()

    df = pd.DataFrame(data)

    # Convert UTC to NYC timezone
    df["date"] = df["date"].dt.tz_convert(NYC_TIMEZONE)
    df["date"] = df["date"].dt.date  # Keep only date part

    return df


def save_weather_data(df, start_date, end_date):
    """Save weather data to CSV."""
    os.makedirs(WEATHER_OUTPUT_DIR, exist_ok=True)

    filename = f"weather_nyc_{start_date}_to_{end_date}.csv"
    filepath = os.path.join(WEATHER_OUTPUT_DIR, filename)

    df.to_csv(filepath, index=False)
    print(f"\nSaved {len(df)} records to {filepath}")
    print(f"\nData summary:")
    print(df.describe())


def main():
    print("=" * 60)
    print("NYC Weather Data Fetcher")
    print("=" * 60)

    # Check if file already exists
    filename = f"weather_nyc_{START_DATE}_to_{END_DATE}.csv"
    filepath = os.path.join(WEATHER_OUTPUT_DIR, filename)

    if os.path.exists(filepath):
        print(f"\nFile already exists: {filepath}")
        response = input("Do you want to re-download? (y/n): ")
        if response.lower() != "y":
            print("Skipping download.")
            return

    # Fetch data
    response = fetch_data(START_DATE, END_DATE)

    if response is None:
        print("Failed to fetch weather data.")
        return

    # Process data
    print("\nProcessing weather data...")
    df = process_data(response)

    # Save data
    save_weather_data(df, START_DATE, END_DATE)

    print("\n" + "=" * 60)
    print("Weather data collection complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
