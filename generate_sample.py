# generate_sample.py
import csv
import sys
from datetime import datetime, timedelta
import random

"""
generate_sample.py

Prompts the user for a start and end date (YYYYMMDD), then
creates a CSV file of sample sales data between those dates.
"""

def prompt_date(prompt_text):
    while True:
        s = input(prompt_text).strip()
        try:
            return datetime.strptime(s, "%Y%m%d").date()
        except ValueError:
            print("Invalid format. Please enter date as YYYYMMDD.")


def generate_rows(start_date, end_date):
    """
    For each date between start_date and end_date inclusive,
    generate a random sales record.
    """
    regions = ["North", "South", "East", "West"]
    products = ["P001", "P002", "P003", "P004", "P005"]
    order_id = int(start_date.strftime("%Y%m%d")) * 1000

    rows = []
    current = start_date
    while current <= end_date:
        for pid in products:
            qty = random.randint(1, 20)
            price = round(random.uniform(5.0, 100.0), 2)
            rows.append((order_id, current.strftime("%Y-%m-%d"), pid,
                         random.choice(regions), qty, price))
            order_id += 1
        current += timedelta(days=1)
    return rows


def write_csv(rows, filename):
    """
    Write out rows to CSV with header.
    """
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["order_id", "sale_date", "product_id", "region", "quantity", "unit_price"])
        writer.writerows(rows)
    print(f"Generated {len(rows)} rows and wrote to {filename}")


def main():
    print("Sample CSV Generator")
    start = prompt_date("Enter start date (YYYYMMDD): ")
    end = prompt_date("Enter end date   (YYYYMMDD): ")
    if end < start:
        print("End date must be on or after start date.")
        sys.exit(1)

    rows = generate_rows(start, end)
    filename = f"sample_{start.strftime('%Y%m%d')}_{end.strftime('%Y%m%d')}.csv"
    write_csv(rows, filename)


if __name__ == "__main__":
    main()
