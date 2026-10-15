import pandas as pd
import mysql.connector
from pathlib import Path

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "processed"

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ecommerce_analytics"
)

print("MySQL connected successfully!")

cursor = connection.cursor()

# Load Calendar CSV
calendar = pd.read_csv(
    PROCESSED_DIR / "calendar_clean.csv"
)

# Only date column
calendar_query = """
INSERT INTO calendar
(date)
VALUES (%s)
"""

calendar_data = [
    (row,)
    for row in calendar["date"]
]

# Load in batches
BATCH_SIZE = 500

for start in range(0, len(calendar_data), BATCH_SIZE):
    end = min(start + BATCH_SIZE, len(calendar_data))

    batch = calendar_data[start:end]

    cursor.executemany(calendar_query, batch)
    connection.commit()

    print(f"Calendar loaded: {end}/{len(calendar_data)}")

cursor.close()
connection.close()

print("\nCalendar loaded successfully!")