import pandas as pd

df = pd.read_csv("flight_delays_raw.csv")
df.columns = df.columns.str.strip()

# Fill missing text values
text_cols = [
    "Airline_Name",
    "Origin_City",
    "Destination_City",
    "Cancellation_Code"
]

for col in text_cols:
    df[col] = df[col].fillna("UNKNOWN")
    df[col] = df[col].astype(str).str.upper().str.strip()
    df[col] = df[col].replace(["???", "N/A", "NAN", ""], "UNKNOWN")

# Fill missing time/delay text columns
df["Actual_Departure_Time"] = df["Actual_Departure_Time"].fillna("00:00")
df["Security_Delay_HH_MM"] = df["Security_Delay_HH_MM"].fillna("00:00")

# Fill missing numeric columns using median
df["Actual_Elapsed_Time_Minutes"] = df["Actual_Elapsed_Time_Minutes"].fillna(
    df["Actual_Elapsed_Time_Minutes"].median()
)

df["Diverted_Flag"] = df["Diverted_Flag"].fillna(0)

# Remove duplicates
df = df.drop_duplicates()

# Keep valid delay ranges
df = df[(df["Departure_Delay_Minutes"] > -60) &
        (df["Departure_Delay_Minutes"] < 1000)]

df = df[(df["Arrival_Delay_Minutes"] > -60) &
        (df["Arrival_Delay_Minutes"] < 1000)]

# Convert date format
df["Flight_Date"] = pd.to_datetime(df["Flight_Date"], errors="coerce")
df = df.dropna(subset=["Flight_Date"])
df["Flight_Date"] = df["Flight_Date"].dt.date

# Check validation
print(df.isnull().sum())
print("Duplicates:", df.duplicated().sum())
print("Rows after cleaning:", len(df))

df.to_csv("flight_delays_cleaned.csv", index=False)

print("Cleaning Done")