"""
clean_data.py
Purpose: Clean flights/airlines/airports CSVs and write a clean Parquet file.
Run:     python src/clean_data.py
"""

import pandas as pd

# ----------------------------------------------------------------------
# 1. LOAD RAW CSVs
# ----------------------------------------------------------------------
print("Loading raw CSVs...")
flights = pd.read_csv("data/flights.csv", low_memory=False)
airlines = pd.read_csv("data/airlines.csv")
airports = pd.read_csv("data/airports.csv")

print(f"  flights:  {flights.shape}")
print(f"  airlines: {airlines.shape}")
print(f"  airports: {airports.shape}")


# ----------------------------------------------------------------------
# 2. DROP UNUSED COLUMNS  (Rule 1)
# ----------------------------------------------------------------------
print("\nDropping unused columns...")
cols_to_drop = [
    "TAIL_NUMBER",
    "WHEELS_OFF",
    "WHEELS_ON",
    "SCHEDULED_TIME",
    "ELAPSED_TIME",
]
flights = flights.drop(columns=cols_to_drop)
print(f"  flights now: {flights.shape[1]} columns")


# ----------------------------------------------------------------------
# 3. BUILD A PROPER DATE COLUMN  (Rule 2)
# ----------------------------------------------------------------------
print("\nBuilding DATE column...")
flights["FLIGHT_DATE"] = pd.to_datetime(
    flights[["YEAR", "MONTH", "DAY"]].rename(
        columns={"YEAR": "year", "MONTH": "month", "DAY": "day"}
    ),
    errors="coerce",
)
print(f"  Sample dates: {flights['FLIGHT_DATE'].head(3).tolist()}")
print(f"  Null dates:   {flights['FLIGHT_DATE'].isnull().sum()}")


# ----------------------------------------------------------------------
# 4. CONVERT FLAGS TO BOOLEANS  (Rule 3)
# ----------------------------------------------------------------------
print("\nConverting flags to booleans...")
flights["CANCELLED"] = flights["CANCELLED"].astype(bool)
flights["DIVERTED"] = flights["DIVERTED"].astype(bool)
print(f"  Cancelled true count: {flights['CANCELLED'].sum()}")


# ----------------------------------------------------------------------
# 5. MAP CANCELLATION REASONS  (Rule 5)
# ----------------------------------------------------------------------
print("\nMapping cancellation reasons...")
reason_map = {
    "A": "Carrier",
    "B": "Weather",
    "C": "National Airspace System",
    "D": "Security",
}
flights["CANCELLATION_REASON"] = flights["CANCELLATION_REASON"].map(reason_map)
print(f"  Sample reasons: {flights['CANCELLATION_REASON'].dropna().unique()}")


# ----------------------------------------------------------------------
# 6. JOIN AIRLINES  (Rule 6)
# ----------------------------------------------------------------------
print("\nJoining airlines...")
flights = flights.merge(
    airlines.rename(columns={"IATA_CODE": "AIRLINE", "AIRLINE": "AIRLINE_NAME"}),
    on="AIRLINE",
    how="left",
)
print(f"  flights now: {flights.shape[1]} columns")


# ----------------------------------------------------------------------
# 7. JOIN ORIGIN AIRPORTS  (Rule 7a)
# ----------------------------------------------------------------------
print("Joining origin airports...")
flights = flights.merge(
    airports[["IATA_CODE", "CITY", "STATE"]].rename(
        columns={
            "IATA_CODE": "ORIGIN_AIRPORT",
            "CITY": "ORIGIN_CITY",
            "STATE": "ORIGIN_STATE",
        }
    ),
    on="ORIGIN_AIRPORT",
    how="left",
)
print(f"  flights now: {flights.shape[1]} columns")


# ----------------------------------------------------------------------
# 8. JOIN DESTINATION AIRPORTS  (Rule 7b)
# ----------------------------------------------------------------------
print("Joining destination airports...")
flights = flights.merge(
    airports[["IATA_CODE", "CITY", "STATE"]].rename(
        columns={
            "IATA_CODE": "DESTINATION_AIRPORT",
            "CITY": "DESTINATION_CITY",
            "STATE": "DESTINATION_STATE",
        }
    ),
    on="DESTINATION_AIRPORT",
    how="left",
)
print(f"  flights now: {flights.shape[1]} columns")


# ----------------------------------------------------------------------
# 9. FILTER OUT UNKNOWN AIRPORTS  (Rule 8)
# ----------------------------------------------------------------------
print("\nFiltering rows with unknown airports...")
before = len(flights)
flights = flights.dropna(subset=["ORIGIN_CITY", "DESTINATION_CITY"])
after = len(flights)
print(f"  Dropped {before - after:,} rows (unknown airports)")
print(f"  Remaining: {after:,} rows")


# ----------------------------------------------------------------------
# 10. SAVE AS PARQUET
# ----------------------------------------------------------------------
print("\nSaving cleaned data to Parquet...")
flights.to_parquet("data/cleaned_flights.parquet", index=False)
print("  Saved: data/cleaned_flights.parquet")
print(f"  Final shape: {flights.shape}")

print("\nDone.")