# Databricks Notebooks

These notebooks run inside Databricks (Free Edition, Serverless Compute).

| Notebook | Purpose |
|----------|---------|
| `01_setup_and_connect.ipynb` | Test Spark + (attempted) S3 connection |
| `02_silver_layer.ipynb` | PySpark cleaning + joins → `silver_flights` Delta table |
| `03_gold_layer.ipynb` | 6 aggregated Delta tables → `gold_*` |

## How to Run

1. Import the `.ipynb` into Databricks (Workspace → Import)
2. Attach to a Serverless compute
3. Verify catalog/schema names match your workspace
4. Run cells top to bottom

## What These Notebooks Produce

- `silver_flights` — 5.3M rows, 32 cols (cleaned + joined)
- `gold_airline_performance` — 14 rows
- `gold_airport_traffic` — ~320 rows
- `gold_monthly_delays` — 12 rows
- `gold_cancellation_reasons` — ~5 rows
- `gold_route_performance` — ~4,500 rows
- `gold_hourly_delays` — 24 rows

## 📓 Databricks Notebooks

The PySpark transformation code lives in Databricks notebooks (exported to `notebooks/`):

- [`02_silver_layer.ipynb`](notebooks/02_silver_layer.ipynb) — cleaning + joins → `silver_flights`
- [`03_gold_layer.ipynb`](notebooks/03_gold_layer.ipynb) — 6 aggregated gold tables

To run them, import into Databricks and attach to a Serverless compute cluster.
See [`notebooks/README.md`](notebooks/README.md) for details.