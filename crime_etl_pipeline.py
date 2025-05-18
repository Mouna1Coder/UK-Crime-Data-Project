import requests
import pandas as pd
import mysql.connector
from mysql.connector import Error

# --- Configuration ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'username',
    'password': 'passoword',
    'database': 'crime_data_api'
}

# London coordinates
LATITUDE = 51.5074
LONGITUDE = -0.1278
DATE = '2023-12'  # Format: YYYY-MM

# --- Extract ---
def fetch_crime_data(lat, lng, date):
    url = f"https://data.police.uk/api/crimes-street/all-crime?lat={lat}&lng={lng}&date={date}"
    response = requests.get(url)

    if response.status_code == 200:
        print("✅ Data fetched from API successfully.")
        return pd.DataFrame(response.json())
    else:
        print("❌ Failed to fetch data:", response.status_code)
        return pd.DataFrame()

# --- Transform ---
def transform_data(df):
    if df.empty:
        return df

    # Flatten location fields and rename columns
    records = []
    for _, row in df.iterrows():
        location = row['location'] or {}
        records.append({
            'id': row.get('id'),
            'month': row.get('month'),
            'category': row.get('category'),
            'location_type': row.get('location_type'),
            'location_description': location.get('street', {}).get('name') if location else None,
            'latitude': float(location.get('latitude', 0)) if location else None,
            'longitude': float(location.get('longitude', 0)) if location else None,
            'context': row.get('context'),
            'persistent_id': row.get('persistent_id'),
            'location_subtype': row.get('location_subtype')
        })
    return pd.DataFrame(records)

# --- Load ---
def load_to_database(df):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Clear the table before inserting new data
        cursor.execute("TRUNCATE TABLE crimes")
        print("🧹 Cleared existing data in the table.")

        insert_query = """
        INSERT IGNORE INTO crimes (
            id, month, category, location_type, location_description,
            latitude, longitude, context, persistent_id, location_subtype
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        for _, row in df.iterrows():
            # Replace NaN with None so MySQL accepts it
            values = tuple(row.where(pd.notnull(row), None))
            cursor.execute(insert_query, values)

        connection.commit()
        print(f"✅ {cursor.rowcount} records inserted into the database.")

    except Error as e:
        print("❌ Database error:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("🔒 Database connection closed.")

# --- Main ---
def main():
    raw_df = fetch_crime_data(LATITUDE, LONGITUDE, DATE)
    cleaned_df = transform_data(raw_df)
    if not cleaned_df.empty:
        load_to_database(cleaned_df)
    else:
        print("No data to load.")

if __name__ == "__main__":
    main()
