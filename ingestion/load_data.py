"""
load_data.py
Loads Olist CSV files from data/raw/ into PostgreSQL staging tables.
Run after: docker-compose up -d
"""

import os
import glob
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/ecommerce")
RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

# Map CSV filename → staging table name
CSV_TABLE_MAP = {
    "olist_orders_dataset.csv":                "stg_orders",
    "olist_order_items_dataset.csv":           "stg_order_items",
    "olist_customers_dataset.csv":             "stg_customers",
    "olist_sellers_dataset.csv":               "stg_sellers",
    "olist_products_dataset.csv":              "stg_products",
    "olist_order_payments_dataset.csv":        "stg_order_payments",
    "olist_order_reviews_dataset.csv":         "stg_order_reviews",
    "product_category_name_translation.csv":   "stg_category_translation",
}


def get_engine():
    engine = create_engine(DATABASE_URL)
    return engine


def load_csv(engine, csv_path: str, table_name: str) -> int:
    df = pd.read_csv(csv_path, low_memory=False)
    df.columns = [c.strip().lower() for c in df.columns]
    df.to_sql(table_name, engine, if_exists="replace", index=False, chunksize=5000)
    return len(df)


def main():
    engine = get_engine()

    # Verify connection
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print(f"Connected to: {DATABASE_URL}\n")

    files_found = glob.glob(os.path.join(RAW_DATA_DIR, "*.csv"))
    if not files_found:
        print(f"No CSV files found in {RAW_DATA_DIR}")
        print("Download the Olist dataset from Kaggle and place CSVs in data/raw/")
        return

    total_rows = 0
    for csv_name, table_name in tqdm(CSV_TABLE_MAP.items(), desc="Loading tables"):
        csv_path = os.path.join(RAW_DATA_DIR, csv_name)
        if not os.path.exists(csv_path):
            print(f"  [SKIP] {csv_name} not found")
            continue
        rows = load_csv(engine, csv_path, table_name)
        total_rows += rows
        print(f"  [OK]   {table_name:35s} {rows:>7,} rows")

    print(f"\nDone. {total_rows:,} total rows loaded.")
    print("Next step: psql $DATABASE_URL -f sql/schema/01_create_tables.sql")


if __name__ == "__main__":
    main()
