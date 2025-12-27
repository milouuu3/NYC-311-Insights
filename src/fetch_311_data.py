import os
import time
import pandas as pd
from sodapy import Socrata
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

START_DATE = "2024-01-01"
END_DATE = "2024-12-31"
BATCH_SIZE = 30  # Fetch in monthly batches
TIMEOUT = 60  # API timeout in seconds
REQUEST_LIMIT = 50000  # Records per API request
OUTPUT_DIR = "data/raw/311"

COLS = [
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


def split_date_batches(start_date, end_date, batch_size):
    """Split the given date range into equal batches"""
    batches = []
    current = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    while current < end:
        batch_end = min(current + timedelta(days=batch_size), end)
        batches.append(
            {"start": current.strftime("%Y-%m-%d"), "end": batch_end.strftime("%Y-%m-%d")}
        )
        current = batch_end

    return batches


def fetch_batch(client, start_date, end_date, offset=0):
    """Fetch one batch from NYC 311 data API"""
    where_clause = (
        f"created_date >= '{start_date}T00:00:00' AND created_date < '{end_date}T23:59:59'"
    )
    select_clause = ",".join(COLS)
    try:
        results = client.get(
            "erm2-nwe9",
            select=select_clause,
            where=where_clause,
            limit=REQUEST_LIMIT,
            offset=offset,
            order="created_date ASC",
        )
        return results
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def save_batch(df, start_date, end_date):
    """Save batch to CSV file."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"311_data_{start_date}_to_{end_date}.csv"
    filepath = os.path.join(OUTPUT_DIR, filename)

    df.to_csv(filepath, index=False)
    print(f"Saved {len(df)} records to {filepath}")


def main():
    print(f"Fetching 311 data from {START_DATE} to {END_DATE}")
    print(f"Output directory: {OUTPUT_DIR}")

    # Initialize client
    client = Socrata("data.cityofnewyork.us", os.getenv("NYC_APP_TOKEN"), timeout=TIMEOUT)

    # Create batches
    batches = split_date_batches(START_DATE, END_DATE, BATCH_SIZE)
    print(f"Total batches to process: {len(batches)}")

    for i, batch in enumerate(batches, 1):
        start = batch["start"]
        end = batch["end"]

        # Check if file already exists
        filename = f"311_data_{start}_to_{end}.csv"
        filepath = os.path.join(OUTPUT_DIR, filename)
        if os.path.exists(filepath):
            print(f"[{i}/{len(batches)}] Skipping {start} to {end} - file already exists")
            continue

        print(f"[{i}/{len(batches)}] Fetching {start} to {end}...")

        all_results = []
        offset = 0

        # Handle pagination
        while True:
            results = fetch_batch(client, start, end, offset)

            if results is None:
                print(f"Failed to fetch batch {start} to {end} at offset {offset}")
                break

            if len(results) == 0:
                break

            all_results.extend(results)
            print(f"  Fetched {len(results)} records (total: {len(all_results)})")

            # If we got less than the limit, we're done with this batch
            if len(results) < REQUEST_LIMIT:
                break

            offset += REQUEST_LIMIT
            time.sleep(1)  # Be nice to the API

        # Save if we got data
        if all_results:
            df = pd.DataFrame.from_records(all_results)
            save_batch(df, start, end)
        else:
            print(f"No data found for {start} to {end}")

        time.sleep(2)  # Pause between batches

    print("\nData collection complete!")
    client.close()


if __name__ == "__main__":
    main()
