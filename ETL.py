 #  Part1- ETL
 # 1.Extract: Collecting Flight Data from Sources
# Import Data


import pandas as pd
import sqlite3
import time
import requests

API_KEY = "YOUR_API_KEY_HERE"
API_URL = "http://api.aviationstack.com/v1/flights"
CSV_FILE_PATH = "flight_delays_cleaned.csv"

DB_PATH = "flights.db"
TABLE_NAME = "flights"


#Extract CSV





def extract_csv(file_path):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    print("Kaggle CSV data extracted successfully")
    return df


# Extract API File



def extract_api_file():
    response = requests.get(API_URL, params={"access_key": API_KEY, "limit": 100})
    response.raise_for_status()
    records = response.json().get("data", [])
    api_data = pd.json_normalize(records)
    print("AviationStack API data extracted successfully (live)")
    return api_data



csv_data = extract_csv(CSV_FILE_PATH)
api_data = extract_api_file() 

print("csv_data loaded:", csv_data.shape)
print("api_data loaded:", api_data.shape)


#2.Transform: Cleaning, Filtering, and Preparing Data Before Loading

# Kaggle Cleaning Function



def clean_kaggle_data(df):
    df = df.copy()

    # Standardize column names
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # Remove duplicates
    df = df.drop_duplicates()

    # Convert date
    df["flight_date"] = pd.to_datetime(df["flight_date"], errors="coerce").dt.date

    # Convert delay columns
    df["departure_delay"] = pd.to_numeric(
        df["departure_delay_minutes"], errors="coerce"
    ).fillna(0)

    df["arrival_delay"] = pd.to_numeric(
        df["arrival_delay_minutes"], errors="coerce"
    ).fillna(0)

    # Convert cancelled and diverted flags
    df["cancelled"] = df["cancelled_flag"].astype(str).str.lower().apply(
        lambda x: 0 if x == "not cancelled" else 1
    )

    df["diverted"] = df["diverted_flag"].astype(str).str.lower().apply(
        lambda x: 0 if x == "not diverted" else 1
    )

    # Create total delay
    df["total_delay"] = df["departure_delay"] + df["arrival_delay"]

    # Create delay status
    df["delay_status"] = df.apply(
        lambda row: "Cancelled" if row["cancelled"] == 1
        else "Diverted" if row["diverted"] == 1
        else "Delayed" if row["total_delay"] > 15
        else "On Time",
        axis=1
    )

    # Add source column
    df["data_source"] = "Kaggle"

    # Rename columns
    df = df.rename(columns={
        "airline_name": "airline",
        "origin_city": "origin_airport",
        "destination_city": "destination_airport"
    })

    # Keep final analytical columns
    final_df = df[
        [
            "flight_date",
            "airline",
            "origin_airport",
            "destination_airport",
            "scheduled_departure_time",
            "actual_departure_time",
            "departure_delay",
            "scheduled_arrival_time",
            "actual_arrival_time",
            "arrival_delay",
            "total_delay",
            "cancelled",
            "diverted",
            "delay_status",
            "data_source"
        ]
    ]

    return final_df


#API Cleaning Function



def clean_api_data(df):
    df = df.copy()

    df.columns = df.columns.str.lower().str.replace(".", "_").str.replace(" ", "_")
    df = df.drop_duplicates()

    cleaned_api = pd.DataFrame()

    cleaned_api["flight_date"] = pd.to_datetime(df["flight_date"], errors="coerce").dt.date
    cleaned_api["airline"] = df["airline_name"].fillna("Unknown")
    cleaned_api["origin_airport"] = df["departure_airport"].fillna("Unknown")
    cleaned_api["destination_airport"] = df["arrival_airport"].fillna("Unknown")

    cleaned_api["scheduled_departure_time"] = df["departure_scheduled"]
    cleaned_api["actual_departure_time"] = df["departure_actual"]
    cleaned_api["scheduled_arrival_time"] = df["arrival_scheduled"]
    cleaned_api["actual_arrival_time"] = df["arrival_actual"]

    cleaned_api["departure_delay"] = pd.to_numeric(df["departure_delay"], errors="coerce").fillna(0)
    cleaned_api["arrival_delay"] = pd.to_numeric(df["arrival_delay"], errors="coerce").fillna(0)

    cleaned_api["cancelled"] = df["flight_status"].astype(str).str.lower().apply(
        lambda x: 1 if x == "cancelled" else 0
    )

    cleaned_api["diverted"] = df["flight_status"].astype(str).str.lower().apply(
        lambda x: 1 if x == "diverted" else 0
    )

    cleaned_api["total_delay"] = cleaned_api["departure_delay"] + cleaned_api["arrival_delay"]

    cleaned_api["delay_status"] = cleaned_api.apply(
        lambda row: "Cancelled" if row["cancelled"] == 1
        else "Diverted" if row["diverted"] == 1
        else "Delayed" if row["total_delay"] > 15
        else "On Time",
        axis=1
    )

    cleaned_api["data_source"] = "AviationStack"

    final_api = cleaned_api[
        [
            "flight_date",
            "airline",
            "origin_airport",
            "destination_airport",
            "scheduled_departure_time",
            "actual_departure_time",
            "departure_delay",
            "scheduled_arrival_time",
            "actual_arrival_time",
            "arrival_delay",
            "total_delay",
            "cancelled",
            "diverted",
            "delay_status",
            "data_source"
        ]
    ]

    return final_api


#Data Transformation




# Standardize column names
csv_data.columns = csv_data.columns.str.lower().str.replace(" ", "_")
api_data.columns = api_data.columns.str.lower().str.replace(".", "_").str.replace(" ", "_")

# Clean each source separately
cleaned_csv = clean_kaggle_data(csv_data)
cleaned_api = clean_api_data(api_data)

# Merge both cleaned datasets
combined_data = pd.concat([cleaned_csv, cleaned_api], ignore_index=True)

# Convert relevant numeric columns
for col in ["departure_delay", "arrival_delay", "total_delay", "cancelled", "diverted"]:
    if col in combined_data.columns:
        combined_data[col] = pd.to_numeric(combined_data[col], errors="coerce").fillna(0)

# Handle missing text values
for col in ["airline", "origin_airport", "destination_airport", "delay_status", "data_source"]:
    if col in combined_data.columns:
        combined_data[col] = combined_data[col].fillna("Unknown")

# Remove duplicate rows
combined_data.drop_duplicates(inplace=True)

print("Data Transformation Completed")
print(combined_data.head())


#Data Before Transformation


csv_data = extract_csv(CSV_FILE_PATH)
api_data = extract_api_file() 

print("Data Before Transformation - Kaggle")
print(csv_data.head())

print("Data Before Transformation - API")
print(api_data.head())


#Data After Transformation


cleaned_csv = clean_kaggle_data(csv_data)
cleaned_api = clean_api_data(api_data)

print("Data After Transformation - Kaggle")
print(cleaned_csv.head())

print("Data After Transformation - API")
print(cleaned_api.head())


#Load: Storing Transformed Data into SQLite




merged_data = pd.concat([cleaned_csv, cleaned_api], ignore_index=True)
merged_data = merged_data.drop_duplicates()
merged_data = merged_data.fillna("Unknown")
print("Merged Data Shape:", merged_data.shape)
print(merged_data.head())

conn = sqlite3.connect("flights.db")
merged_data.to_sql("flights", conn, if_exists="replace", index=False)
conn.close()

print("Final ETL data loaded successfully into flights.db")

conn = sqlite3.connect(DB_PATH)
merged_data.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)
conn.close()

print("Data loaded successfully into SQLite")


#Workflow Automation



def main():
    print("Starting ETL process...")
 # Start ETL timer
    etl_start = time.time()
    
    csv_data = extract_csv(CSV_FILE_PATH)
    api_data = extract_api_file()

    cleaned_csv = clean_kaggle_data(csv_data)
    cleaned_api = clean_api_data(api_data)

    merged_data = pd.concat([cleaned_csv, cleaned_api], ignore_index=True)
    merged_data = merged_data.drop_duplicates()
    merged_data = merged_data.fillna("Unknown")

    conn = sqlite3.connect(DB_PATH)
    merged_data.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)
    conn.close()

    print("ETL Process Completed!")
    etl_end = time.time()

    print("\nFinal ETL data loaded successfully into flights.db")
    print("ETL Process Completed!")
    print("ETL Execution Time:", round(etl_end - etl_start, 4), "seconds")
if __name__ == "__main__":
    main()
 
# ------ for code in sqile --------
# cd C:\sqlite 
#sqlite3 C:\Users\leena\venv\flights.db
# .tables
# SELECT * FROM flights LIMIT 10;





