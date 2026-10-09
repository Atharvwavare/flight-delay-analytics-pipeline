"""
upload_to_s3.py
Purpose: Upload raw CSVs and cleaned Parquet to S3.
Run:     python src/upload_to_s3.py
"""

import os
import boto3
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Create S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

bucket = os.getenv("S3_BUCKET")
print(f"Target bucket: {bucket}")

# Define what to upload
files_to_upload = {
    # Raw CSVs → raw/ folder
    "data/flights.csv": "raw/flights/flights.csv",
    "data/airlines.csv": "raw/airlines/airlines.csv",
    "data/airports.csv": "raw/airports/airports.csv",
    # Cleaned Parquet → silver/ folder
    "data/cleaned_flights.parquet": "silver/flights/cleaned_flights.parquet",
}

# Upload each file
for local_path, s3_key in files_to_upload.items():
    if not os.path.exists(local_path):
        print(f"  SKIP (not found): {local_path}")
        continue

    size_mb = os.path.getsize(local_path) / (1024 * 1024)
    print(f"  Uploading {local_path} ({size_mb:.1f} MB) → s3://{bucket}/{s3_key}")

    s3.upload_file(local_path, bucket, s3_key)

print("\nAll uploads complete.")