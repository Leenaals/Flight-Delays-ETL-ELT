# ELT
# 1. Raw Data Sources Overview

import pandas as pd
from sqlalchemy import create_engine, text
import time
start_time = time.time()

KAGGLE_RAW_FILE = "Flight_Delays_raw.csv"
API_RAW_FILE = "api_flights.csv"

df_kaggle = pd.read_csv(KAGGLE_RAW_FILE)
df_api = pd.read_csv(API_RAW_FILE)

print("Kaggle Raw Data:", df_kaggle.shape)
print("API Raw Data:", df_api.shape)

print("\nKaggle Head:")
print(df_kaggle.head())

print("\nAPI Head:")
print(df_api.head())


# =========================
# 2. Load Raw Data into Neon
# =========================

NEON_CONNECTION_STRING = "YOUR_NEON_CONNECTION_STRING_HERE"

engine = create_engine(NEON_CONNECTION_STRING)

# Load raw tables first
df_kaggle.to_sql("stage_kaggle_raw", engine, if_exists="replace", index=False)

df_api.to_sql("stage_api_raw", engine, if_exists="replace", index=False)

print("\nRaw data loaded into Neon successfully.")


# =========================
# 3. Transform Data Inside Neon
# =========================


# =========================
# 4. Export Final Data
# =========================

df_elt = pd.read_sql("SELECT * FROM final_flight_delays", engine)

df_elt.to_csv("elt_flight_dashboard.csv", index=False, encoding="utf-8-sig")

df_elt.to_excel("elt_flight_dashboard.xlsx", index=False)

print("\nELT dashboard files exported successfully.")

print(df_elt.shape)

print(df_elt.head())
end_time = time.time()

execution_time = end_time - start_time

print(f"ELT Execution Time: {execution_time:.4f} seconds")


