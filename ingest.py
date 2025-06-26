#ingest.py
import csv
import io
import sys
import logging
from datetime import datetime

import psycopg, os

# DSN pointing at your Docker‐Compose Postgres service
DB_DSN = os.getenv(
    "DB_DSN",
    "postgresql://analytics_user:analytics_pass@postgresql:5432/analytics"
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ingest")   

def validate_row(row):
    """
    Parse & validate a single CSV row. Returns a tuple of values
    or None if invalid (and logs the error).
    """
    try:
        return (
            int(row["order_id"]),
            datetime.strptime(row["sale_date"], "%Y-%m-%d").date(),
            row["product_id"],
            row["region"],
            int(row["quantity"]),
            float(row["unit_price"]),
        )
    except Exception:
        return None


def main(csv_path, batch_size=1000):
    # Connect to Postgres
    conn = psycopg.connect(DB_DSN)
    cur = conn.cursor()
    inserted = 0

    try:
        with open(csv_path, newline="") as f:
            for row in csv.DictReader(f):
                vals = validate_row(row)
                if vals is None:
                    continue
                cur.execute(
                    "INSERT INTO sales"
                    " (order_id, sale_date, product_id, region, quantity, unit_price)"
                    " VALUES (%s, %s, %s, %s, %s, %s)",
                    vals
                )
                inserted += 1
        conn.commit()
        print(f"Inserted {inserted} rows into sales table.")
    except FileNotFoundError:
        print(f"Error: file not found: {csv_path}")
        sys.exit(1)
    except Exception as e:
        conn.rollback()
        print(f"Insertion failed: {e}")
        sys.exit(1)
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ingest.py path/to/your.csv")
        sys.exit(1)
    main(sys.argv[1])
