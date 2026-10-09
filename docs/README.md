# ✈️ Flight Delay Analytics Pipeline

An end-to-end data engineering pipeline analyzing **5.3 million U.S. flights in 2015**, built with PySpark, Delta Lake, AWS S3, and Databricks SQL.

**[📊 Dashboard Screenshots](docs/screenshots/)** · **[🏗️ Architecture](docs/architecture.md)** · **[📖 Data Dictionary](docs/data_dictionary.md)** · **[📋 Pipeline Log](docs/pipeline_log.md)**

---

## 📸 Dashboard Preview

![Flight Delay Dashboard](docs/screenshots/dashboard_full.png)

*11-widget dashboard showing airline reliability, airport traffic, monthly trends, cancellations, route performance, and hourly delay patterns.*

---

## 🎯 Business Questions Answered

1. Which airlines are most on time?
2. Which airports handle the most traffic?
3. How do delays trend across 2015?
4. What are the main causes of cancellations?
5. Which origin → destination routes have the worst delays?
6. What time of day has the worst delays?

---

## 🏗️ Architecture

```
Kaggle CSVs → S3 (raw) → Databricks Silver (PySpark) → Databricks Gold → SQL Dashboard
```

See [docs/architecture.md](docs/architecture.md) for the full diagram and layer-by-layer breakdown.

---

## 🛠️ Tech Stack

| Layer | Tool |
|-------|------|
| **IDE** | PyCharm |
| **Local processing** | Python (pandas, boto3) |
| **Cloud storage** | AWS S3 |
| **Cloud compute** | Databricks (Serverless) |
| **Big data processing** | PySpark |
| **Storage format** | Delta Lake |
| **Catalog** | Unity Catalog |
| **Dashboarding** | Databricks SQL |
| **Version control** | Git + GitHub |

---

## 📁 Project Structure

```
Flight_Delay_Analytics_Pipeline/
├── data/                       # Raw CSVs (gitignored)
├── src/                        # Local Python scripts
│   ├── explore_data.py
│   ├── verify_data.py
│   ├── clean_data.py
│   ├── verify_clean.py
│   ├── view_parquet.py
│   └── upload_to_s3.py
├── airflow/                    # Airflow DAGs (Step 11)
├── notebooks/                  # Notebook exports from Databricks
├── docs/
│   ├── data_dictionary.md
│   ├── pipeline_log.md
│   ├── architecture.md
│   └── screenshots/
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🔄 Pipeline Stages

| Stage | Description | Output |
|-------|-------------|--------|
| 1. Explore | Understand structure of 3 CSVs | `docs/data_dictionary.md` |
| 2. Clean (local) | pandas cleaning + type casting | `cleaned_flights.parquet` |
| 3. Upload | Push raw + cleaned to AWS S3 | `s3://bucket/raw/`, `s3://bucket/silver/` |
| 4. Silver | PySpark cleaning + joins in Databricks | `silver_flights` Delta table |
| 5. Gold | 6 aggregated Delta tables | `gold_*` tables |
| 6. Dashboard | Databricks SQL visualizations | 11 widgets |

---

## 🚀 How to Run

### Prerequisites

- Python 3.11+
- AWS account (free tier)
- Databricks Free Edition account

### Local setup

```bash
git clone <repo-url>
cd Flight_Delay_Analytics_Pipeline
python -m venv .venv
.venv\Scripts\Activate.ps1         # Windows
pip install -r requirements.txt
```

### Run the pipeline

```bash
python src/explore_data.py         # Step 1: explore
python src/clean_data.py           # Step 2: clean locally
python src/upload_to_s3.py         # Step 3: upload to S3
```

Steps 4–6 run **inside Databricks** (notebooks `02_silver_layer` and `03_gold_layer`) — see [docs/pipeline_log.md](docs/pipeline_log.md) for details.

### Environment variables

Create `.env` in project root:

```
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
S3_BUCKET=flight-delay-analytics-yourname
```

---

## 📊 Key Findings

- **Southwest and Delta** have the best on-time rates (~70%)
- **Atlanta (ATL)** is the busiest airport with ~690K total flights
- Delays **peak in June/July** and **December**
- **~40% of cancellations** are airline-caused (Carrier reason)
- Delays **compound through the day** — worst at 7–8 PM
- **Chicago O'Hare (ORD)** routes have the highest average delays

---

## 📝 Documentation

- [Data Dictionary](docs/data_dictionary.md) — every column explained
- [Pipeline Log](docs/pipeline_log.md) — chronological build log
- [Architecture](docs/architecture.md) — full pipeline diagram

---

## 📄 License

MIT — see [LICENSE](LICENSE) file.

---

## 👤 Author

**Atharv Wavare** — Data Engineering Portfolio Project