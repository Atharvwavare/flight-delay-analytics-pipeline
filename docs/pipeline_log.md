# Pipeline Log

Chronological record of what was built, when, and why.
One section per step. Newest at the bottom.

---

## Step 1 — Dataset Exploration (completed)

**Script:** `src/explore_data.py`
**Outcome:** Understood structure of the 3 CSVs.
**Findings documented in:** `docs/data_dictionary.md`

---

## Step 2 — Data Dictionary (completed)

**File:** `docs/data_dictionary.md`
**Outcome:** Documented all columns, join keys, measures, and business questions.
**Helper script:** `src/verify_data.py`

---

## Step 3 — Local Cleaning (completed)

**Script:** `src/clean_data.py`

**Input:**
- `data/flights.csv` (5.8M rows, 31 cols)
- `data/airlines.csv` (14 rows)
- `data/airports.csv` (~322 rows)

**Output:** `data/cleaned_flights.parquet` (~5.8M rows, 30 cols)

**Cleaning rules applied:**
1. Dropped columns: TAIL_NUMBER, WHEELS_OFF, WHEELS_ON, SCHEDULED_TIME, ELAPSED_TIME
2. Built `FLIGHT_DATE` from YEAR + MONTH + DAY
3. Converted `CANCELLED`, `DIVERTED` to booleans
4. Left delay-column nulls untouched (nulls are logical, not errors)
5. Mapped CANCELLATION_REASON: A→Carrier, B→Weather, C→NAS, D→Security
6. Joined airlines → added `AIRLINE_NAME`
7. Joined airports twice → added ORIGIN_CITY/STATE, DESTINATION_CITY/STATE
8. Dropped rows where origin/destination airport was unknown

**Verification scripts:**
- `src/verify_clean.py` — checks shape, dates, nulls, value counts
- `src/view_parquet.py` — prints head/tail/sample and column info

**Why Parquet:** 10× smaller than CSV, 5× faster to read, preserves data types.

---

## Step 4 — AWS S3 Setup (completed)

**Script:** `src/upload_to_s3.py`
**S3 bucket:** `flight-delay-analytics-yourname`
**Region:** us-east-1

**Uploaded:**
- raw/flights/flights.csv
- raw/airlines/airlines.csv
- raw/airports/airports.csv
- silver/flights/cleaned_flights.parquet

**IAM user:** `flight-pipeline-user` (AmazonS3FullAccess)
**Credentials stored in:** `.env` (gitignored)

---

## Step 5 — Databricks Setup + Data Ingestion (completed)

**Platform:** Databricks Free Edition (Serverless)
**Compute:** Serverless Starter Warehouse
**Catalog:** `flights_delay_pipeline`
**Schema:** `flights_schema`

**Tables created (Delta):**
- `raw_flights`
- `airlines`
- `airports`

**Notes:** Direct S3 `spark.conf.set()` not supported on Serverless. Used Unity Catalog managed tables instead — cleaner and production-style.

---

## Step 6 — Silver Layer in PySpark (completed)

**Notebook:** `02_silver_layer`
**Input:** raw_flights, airlines, airports (Unity Catalog Delta tables)
**Output:** `flights_delay_pipeline.flights_schema.silver_flights`

**Final shape:** 5,332,914 rows × 32 cols

**Final columns (32):**
DESTINATION_AIRPORT, ORIGIN_AIRPORT, AIRLINE, YEAR, MONTH, DAY, DAY_OF_WEEK,
FLIGHT_NUMBER, SCHEDULED_DEPARTURE, DEPARTURE_TIME, DEPARTURE_DELAY, TAXI_OUT,
AIR_TIME, DISTANCE, TAXI_IN, SCHEDULED_ARRIVAL, ARRIVAL_TIME, ARRIVAL_DELAY,
DIVERTED, CANCELLED, CANCELLATION_REASON, AIR_SYSTEM_DELAY, SECURITY_DELAY,
AIRLINE_DELAY, LATE_AIRCRAFT_DELAY, WEATHER_DELAY, FLIGHT_DATE, AIRLINE_NAME,
ORIGIN_CITY, ORIGIN_STATE, DESTINATION_CITY, DESTINATION_STATE

**Transformations applied:**
1. Dropped unused columns (TAIL_NUMBER, WHEELS_OFF, WHEELS_ON, SCHEDULED_TIME, ELAPSED_TIME)
2. Built FLIGHT_DATE from YEAR + MONTH + DAY
3. Cast CANCELLED, DIVERTED to boolean
4. Mapped CANCELLATION_REASON to human-readable text
5. Joined airlines → AIRLINE_NAME
6. Joined airports twice → ORIGIN_CITY/STATE, DESTINATION_CITY/STATE
7. Filtered out rows where BOTH origin AND destination were unresolvable

**Debug notes:**
- **Bug 1:** `UNRESOLVED_USING_COLUMN_FOR_JOIN` when chaining `withColumnRenamed` on airlines. Fixed with `select(col(...).alias(...))` for atomic rename.
- **Bug 2:** Initial filter dropped 486,165 rows because ~486K flights in the source CSV have numeric airport codes (like "10135") that don't exist in `airports.csv`. Fixed by filtering only when BOTH origin AND destination are unresolvable — this represents the dataset's genuine data quality issue.

---

## Step 7 — Gold Layer (completed)

**Notebook:** `03_gold_layer`
**Input:** silver_flights (5,332,914 rows)
**Output:** 6 gold Delta tables

| Table | Business question | Rows |
|-------|-------------------|------|
| gold_airline_performance | Which airlines are on time? | 14 |
| gold_airport_traffic | Which airports are busiest? | ~320 |
| gold_monthly_delays | Delay trends across 2015 | 12 |
| gold_cancellation_reasons | Why are flights cancelled? | ~5 |
| gold_route_performance | Worst origin→destination routes | ~4,500 |
| gold_hourly_delays | Which hour of day has worst delays? | 24 |

**Key transformations:**
- filter → groupBy → agg → withColumn → orderBy pattern
- Conditional counting: `when(cond, 1).otherwise(0)` inside `sum`
- `unionByName` for airport traffic (origin + destination)
- Min-flight threshold (>= 100) on routes to avoid statistical noise
- HHMM → hour conversion: `floor(SCHEDULED_DEPARTURE / 100)`

**HHMM time handling:**
- SCHEDULED_DEPARTURE = 1935 → 19:35 (7:35 PM)
- Stored as integer in silver, converted to hour in gold_hourly_delays
- Full timestamps not required for our business questions

---

## Step 8 — Databricks SQL Dashboard (completed)

**Dashboard name:** Flight Delay Analytics 2015
**Platform:** Databricks SQL (Free Edition)
**Data source:** 6 gold tables from Step 7

**Widgets built:**
- 4 KPI counters (Total Flights, Avg Delay, On-Time %, Cancellations)
- Chart: Airline on-time % (bar)
- Chart: Top 15 airports (horizontal bar)
- Chart: Monthly delay trend (line)
- Chart: Cancellation reasons (pie)
- Table: Worst 20 routes
- Chart: Delays by hour of day (area/bar)
- Map: Airport traffic (lat/lon dots on U.S. map)

**Notes:**
- Databricks SQL does not support per-row images (no airline logos)
- Used emoji + Markdown for section headers
- Screenshots saved to `docs/screenshots/` for portfolio

---

## Step 9 — Documentation & Architecture (completed)

**Files created/updated:**
- `README.md` — full rewrite with dashboard screenshot, architecture, key findings
- `docs/architecture.md` — Mermaid pipeline diagram + layer explanations
- `docs/data_dictionary.md` — added Star Schema Design section
- `docs/pipeline_log.md` — this file
- `LICENSE` — MIT
- `.gitignore` — verified (secrets + data excluded)
- `requirements.txt` — cleaned to core dependencies

**Screenshots:** Dashboard screenshots saved to `docs/screenshots/`

**Status:** Repo is portfolio-ready. Next step is pushing to GitHub.

**Next:** Step 10 — Push to GitHub + portfolio polish

---

## Step 10 — GitHub Push + Portfolio Polish (completed)

**Repository:** https://github.com/YOUR-USERNAME/flight-delay-analytics-pipeline

**Actions:**
- Initialized local Git repo
- Verified `.gitignore` excludes secrets, data, venv
- Committed 40+ files
- Created GitHub repo (public, no auto-README)
- Pushed `main` branch
- Added repo description + topics
- Verified no secrets leaked (searched for `.env`, `AKIA`)
- Confirmed Mermaid diagram renders on GitHub
- Confirmed dashboard screenshot renders in README

**Repo status:** Public, portfolio-ready.

**Next (optional):** Step 11 — Airflow orchestration