#ingest.py
import csv
import io
import sys
import logging
from datetime import datetime

import psycopg

# DSN pointing at your Docker‐Compose Postgres service
DB_DSN = "postgresql://analytics_user:analytics_pass@postgres:5432/analytics"

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
    except Exception as e:
        logger.error(f"Skipping row {row!r}: {e}")
        return None


def bulk_insert(conn, rows):
    """
    Use PostgreSQL COPY FROM STDIN for bulk load.
    `rows` should be an iterable of validated tuples.
    """
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerows(rows)
    buffer.seek(0)

    with conn.cursor() as cur:
        cur.copy(
            "COPY sales (order_id, sale_date, product_id, region, quantity, unit_price) "
            "FROM STDIN WITH CSV",
            buffer
        )
    conn.commit()


def main(csv_path, batch_size=1000):
    logger.info(f"Connecting to database: {DB_DSN}")
    conn = psycopg.connect(DB_DSN)
    conn.autocommit = False

    batch = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            v = validate_row(row)
            if v is not None:
                batch.append(v)
            if len(batch) >= batch_size:
                bulk_insert(conn, batch)
                logger.info(f"Inserted {len(batch)} rows")
                batch.clear()

    if batch:
        bulk_insert(conn, batch)
        logger.info(f"Inserted final {len(batch)} rows")

    conn.close()
    logger.info("Ingestion complete.")


main('sample.csv')
