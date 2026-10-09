# Data Dictionary — Flight Delay Analytics

Source: Kaggle "2015 Flight Delays and Cancellations"
Year covered: 2015
Files: flights.csv, airlines.csv, airports.csv

---

## File 1 — flights.csv (FACT TABLE)

**What it is:** One row per flight in 2015. This is the main table of the entire pipeline.

**Row count (full file):** ~5,800,000
**Column count:** 31
**Sampled for exploration:** first 100,000 rows

### Columns

| Column | Type | Meaning | Nulls? | Role |
|--------|------|---------|--------|------|
| YEAR | int | Flight year (2015) | No | Dimension (time) |
| MONTH | int | Flight month (1-12) | No | Dimension (time) |
| DAY | int | Day of month (1-31) | No | Dimension (time) |
| DAY_OF_WEEK | int | 1=Monday ... 7=Sunday | No | Dimension (time) |
| AIRLINE | string | Airline code (joins to airlines.csv) | No | **JOIN KEY** |
| FLIGHT_NUMBER | int | Flight number | No | Attribute |
| TAIL_NUMBER | string | Aircraft registration | Some | Attribute |
| ORIGIN_AIRPORT | string | Origin airport code (joins to airports.csv) | No | **JOIN KEY** |
| DESTINATION_AIRPORT | string | Destination airport code (joins to airports.csv) | No | **JOIN KEY** |
| SCHEDULED_DEPARTURE | int (HHMM) | Scheduled departure time | No | Attribute |
| DEPARTURE_TIME | float (HHMM) | Actual departure time | Many | Attribute |
| DEPARTURE_DELAY | float (min) | Departure delay in minutes | Many | **MEASURE** |
| TAXI_OUT | float (min) | Time between gate and takeoff | Many | Measure |
| WHEELS_OFF | float (HHMM) | Wheels-off time | Many | Attribute |
| SCHEDULED_TIME | float (min) | Scheduled flight duration | No | Attribute |
| ELAPSED_TIME | float (min) | Actual flight duration | Many | Measure |
| AIR_TIME | float (min) | Time in the air | Many | Measure |
| DISTANCE | int (miles) | Distance between airports | No | Measure |
| WHEELS_ON | float (HHMM) | Wheels-on time | Many | Attribute |
| TAXI_IN | float (min) | Time between landing and gate | Many | Measure |
| SCHEDULED_ARRIVAL | int (HHMM) | Scheduled arrival time | No | Attribute |
| ARRIVAL_TIME | float (HHMM) | Actual arrival time | Many | Attribute |
| ARRIVAL_DELAY | float (min) | Arrival delay in minutes | Many | **MEASURE** |
| DIVERTED | int (0/1) | Was the flight diverted? | No | Flag |
| CANCELLED | int (0/1) | Was the flight cancelled? | No | **FLAG** |
| CANCELLATION_REASON | string (A/B/C/D) | A=Carrier, B=Weather, C=NAS, D=Security | ~98% null | Attribute |
| AIR_SYSTEM_DELAY | float (min) | Delay caused by air system | ~98% null | Measure |
| SECURITY_DELAY | float (min) | Delay caused by security | ~98% null | Measure |
| AIRLINE_DELAY | float (min) | Delay caused by airline | ~98% null | Measure |
| LATE_AIRCRAFT_DELAY | float (min) | Delay caused by late aircraft | ~98% null | Measure |
| WEATHER_DELAY | float (min) | Delay caused by weather | ~98% null | Measure |

### Key observations

- **Delay columns are null for cancelled flights** — this is logical, not a bug
- **Cancellation reason is null for non-cancelled flights** — also logical
- Delay-related columns (`AIR_SYSTEM_DELAY`, etc.) only populate when a flight is delayed > 15 min
- Times like `SCHEDULED_DEPARTURE` are stored as `HHMM` integers (e.g., 1430 = 2:30 PM), **not** real timestamps

---

## File 2 — airlines.csv (DIMENSION TABLE)

**What it is:** Maps airline codes to airline names.

**Row count:** 14
**Column count:** 2

| Column | Type | Meaning | Nulls? | Role |
|--------|------|---------|--------|------|
| IATA_CODE | string | 2-letter airline code | No | **JOIN KEY** (joins to flights.AIRLINE) |
| AIRLINE | string | Full airline name | No | Attribute |

### Key observations

- Tiny lookup table
- No nulls
- Join key: `flights.AIRLINE` → `airlines.IATA_CODE`

---

## File 3 — airports.csv (DIMENSION TABLE)

**What it is:** Maps airport codes to location information.

**Row count:** ~322
**Column count:** 7

| Column | Type | Meaning | Nulls? | Role |
|--------|------|---------|--------|------|
| IATA_CODE | string | 3-letter airport code | No | **JOIN KEY** (joins to flights.ORIGIN_AIRPORT / DESTINATION_AIRPORT) |
| AIRPORT | string | Full airport name | No | Attribute |
| CITY | string | City | No | Attribute |
| STATE | string | State code | No | Attribute |
| COUNTRY | string | Country | No | Attribute |
| LATITUDE | float | Latitude | Some | Attribute |
| LONGITUDE | float | Longitude | Some | Attribute |

### Key observations

- Join key `IATA_CODE` used **twice** in flights (origin + destination)
- A few missing lat/lon (usually small regional airports)

---

## Join Map

```
flights.AIRLINE             → airlines.IATA_CODE
flights.ORIGIN_AIRPORT      → airports.IATA_CODE  (as origin)
flights.DESTINATION_AIRPORT → airports.IATA_CODE  (as destination)
```

---

## Column Role Legend

- **JOIN KEY** — used to link tables
- **MEASURE** — numeric columns we aggregate (sum, avg)
- **FLAG** — binary 0/1 indicators
- **Attribute** — descriptive, kept but not aggregated
- **Dimension (time)** — used for grouping by date

---

## Business Questions This Pipeline Answers

1. Which airline has the highest average departure delay?
2. Which airports have the most cancellations?
3. What is the trend of delays across months in 2015?
4. What are the top reasons for cancellations?
5. Which routes (origin → destination) have the worst on-time performance?

---

## Star Schema Design

### Fact Table

- **silver_flights** — one row per flight, contains all measures
  (`DEPARTURE_DELAY`, `ARRIVAL_DELAY`, `AIR_TIME`, `TAXI_OUT`, `TAXI_IN`, `DISTANCE`, etc.)

### Dimension Tables

- **airlines** — airline code → name lookup
- **airports** — airport code → city, state, country, lat/lon lookup

### Foreign Key Relationships

```
silver_flights.AIRLINE             → airlines.IATA_CODE
silver_flights.ORIGIN_AIRPORT      → airports.IATA_CODE   (as origin)
silver_flights.DESTINATION_AIRPORT → airports.IATA_CODE   (as destination)
```

### Why One Fact Table?

All three core entities (flights, delays, cancellations) share the **same grain** (one row per flight), so they live in one wide fact table for simplicity and query performance. In enterprise systems with 100+ columns, they'd be split into separate fact tables.

### Grain

**One row per scheduled flight in 2015.** Every measure (delay, air time, distance) applies to that single flight.

---

## Cleaning Rules (Silver Layer)

1. Drop columns we don't need: TAIL_NUMBER, WHEELS_OFF, WHEELS_ON, SCHEDULED_TIME, ELAPSED_TIME
2. Build a proper DATE column from YEAR + MONTH + DAY
3. Convert CANCELLED and DIVERTED to booleans (True/False)
4. Keep delay columns as floats but leave nulls as nulls (do NOT fill with 0 — null means "not applicable", not "zero delay")
5. Map CANCELLATION_REASON codes: A→Carrier, B→Weather, C→National Airspace System, D→Security
6. Join airlines.csv to add AIRLINE_NAME column
7. Join airports.csv TWICE to add ORIGIN_CITY and DESTINATION_CITY
8. Filter out rows where BOTH origin AND destination airport are unknown