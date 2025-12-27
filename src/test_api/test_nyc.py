import os
import pandas as pd
from sodapy import Socrata
from dotenv import load_dotenv

load_dotenv()

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.cityofnewyork.us", os.getenv("NYC_APP_TOKEN"))

# Example authenticated client (needed for non-public datasets):
# client = Socrata(data.cityofnewyork.us,
#                  MyAppToken,
#                  username="user@example.com",
#                  password="AFakePassword")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
# results = client.get("erm2-nwe9", limit=1)
results = client.get("erm2-nwe9", limit=1, where="created_date > '2024-12-01'")

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
print(results_df)
