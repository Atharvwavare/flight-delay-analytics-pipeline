"""
verify_clean.py
Purpose: Read back the cleaned Parquet and sanity check it.
Run:     python src/verify_clean.py
"""

import pandas as pd

# ----------------------------------------------------------------------
# 1. LOAD CLEANED PARQUET
# ----------------------------------------------------------------------
print("Loading cleaned Parquet...")
df = pd.read_parquet("data/cleaned_flights.parquet")

print(f"\nShape: {df.shape}")
print(f"\nColumns ({len(df.columns)}):\n  {list(df.columns)}")


# ----------------------------------------------------------------------
# 2. DATE RANGE CHECK
# ----------------------------------------------------------------------
print("\n=== Date range ===")
print(f"  Min: {df['FLIGHT_DATE'].min()}")
print(f"  Max: {df['FLIGHT_DATE'].max()}")
print(f"  Null dates: {df['FLIGHT_DATE'].isnull().sum()}")


# ----------------------------------------------------------------------
# 3. TOP AIRLINES BY FLIGHT COUNT
# ----------------------------------------------------------------------
print("\n=== Top 10 airlines by flight count ===")
print(df["AIRLINE_NAME"].value_counts().head(10))


# ----------------------------------------------------------------------
# 4. CANCELLATION REASONS
# ----------------------------------------------------------------------
print("\n=== Cancellation reasons (all values) ===")
print(df["CANCELLATION_REASON"].value_counts(dropna=False))


# ----------------------------------------------------------------------
# 5. TOP ORIGIN CITIES
# ----------------------------------------------------------------------
print("\n=== Top 10 origin cities ===")
print(df["ORIGIN_CITY"].value_counts().head(10))


# ----------------------------------------------------------------------
# 6. NULL COUNTS (top 15 columns)
# ----------------------------------------------------------------------
print("\n=== Null counts (top 15) ===")
print(df.isnull().sum().sort_values(ascending=False).head(15))


# ----------------------------------------------------------------------
# 7. DATA TYPES
# ----------------------------------------------------------------------
print("\n=== Data types ===")
print(df.dtypes)


# ----------------------------------------------------------------------
# 8. QUICK SANITY CHECKS
# ----------------------------------------------------------------------
print("\n=== Sanity checks ===")
print(f"  Total rows:            {len(df):,}")
print(f"  Cancelled flights:     {df['CANCELLED'].sum():,}")
print(f"  Diverted flights:      {df['DIVERTED'].sum():,}")
print(f"  Unique airlines:       {df['AIRLINE_NAME'].nunique()}")
print(f"  Unique origin cities:  {df['ORIGIN_CITY'].nunique()}")
print(f"  Unique destinations:   {df['DESTINATION_CITY'].nunique()}")
print(f"  Avg departure delay:   {df['DEPARTURE_DELAY'].mean():.2f} min")
print(f"  Avg arrival delay:     {df['ARRIVAL_DELAY'].mean():.2f} min")

print("\nDone.")