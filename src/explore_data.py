"""
explore_data.py
Purpose: Peek at the three raw CSVs before doing any pipeline work.
Run:     python src/explore_data.py
"""

import pandas as pd

# Only sample flights.csv — it's 5.8M rows, loading it all takes RAM and time
flights = pd.read_csv("data/flights.csv", nrows=100_000)
airlines = pd.read_csv("data/airlines.csv")
airports = pd.read_csv("data/airports.csv")
print(flights.shape)
datasets = {
    "flights (first 100k rows)": flights,
    "airlines (full)": airlines,
    "airports (full)": airports,
}

for name, df in datasets.items():
    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)
    print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"\nColumns:\n  {list(df.columns)}")
    print(f"\nNull counts per column:\n{df.isnull().sum()}")
    print(f"\nFirst 5 rows:\n{df.head()}")