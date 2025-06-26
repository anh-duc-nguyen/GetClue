<!-- README.md -->
THIS IS A DEMO PROJECT for getclue.com

Problem 2: Optimized Data Aggregation API

Objective: Build a Python application that ingests CSV data into a SQL database (SQLite or PostgreSQL) and provides optimized analytical reports through API endpoints.

Requirements:

Data Ingestion:

A script to load CSV data into the database with validation and error handling.

Analytical Endpoints:

Provide API endpoints for generating:

Monthly sales summaries with optimized query execution.

Filtering by product, region, and date ranges, ensuring queries scale well with large datasets.

A ranking of the top 5 products by revenue, ensuring index usage.

Performance Optimization:

Optimize database schema design to support efficient queries.

Use indexing, partitions, or query caching where applicable.

Measure and document query performance improvements (e.g., before/after execution times).

Constraints:

Use explicit SQL queries for analytical endpoints (avoid ORMs for reporting queries).

Provide clear and meaningful unit tests for query performance validation.

Include a document summarizing performance optimizations made.

Submission:

Provide your submission via a GitHub repository.

Include instructions to run the application and ingest CSV data.

Document how you optimized query execution and performance.

-----
I think firstly let try to create an example inpot csv first and potentially this will be exported out by an excel spreedsheet to a csv file.
asking gpt4o and so something like this:
------sample.csv------
order_id,sale_date,product_id,product_name,region,quantity,unit_price
1001,2025-01-05,P001,Widget A,North,  5,20.00
1002,2025-01-07,P002,Widget B,South,  3,35.00
1003,2025-01-12,P001,Widget A,East,   7,20.00
1004,2025-01-22,P003,Widget C,North, 10,15.00
1005,2025-02-02,P002,Widget B,West,   2,35.00
1006,2025-02-08,P004,Widget D,South,  1,50.00
1007,2025-02-14,P001,Widget A,East,   4,20.00
1008,2025-02-21,P003,Widget C,West,   6,15.00
1009,2025-03-03,P002,Widget B,North,  8,35.00
1010,2025-03-15,P005,Widget E,South, 12,10.00


order_id,sale_date,product_id,product_name,region,quantity,unit_price


Setup postgres

docker exec -it post_gres psql \
  -U analytics_user \
  -d analytics_pass



CREATE TABLE IF NOT EXISTS sales (
    order_id   BIGINT      PRIMARY KEY,
    sale_date  DATE        NOT NULL,
    product_id TEXT        NOT NULL,
    region     TEXT        NOT NULL,
    quantity   INTEGER     NOT NULL,
    unit_price NUMERIC(10,2) NOT NULL
    );

<!-- Track ingestions -->
CREATE TABLE IF NOT EXISTS ingestion_log (
    id             SERIAL   PRIMARY KEY,
    file_name      TEXT     NOT NULL,
    processed_at   TIMESTAMP NOT NULL DEFAULT NOW(),
    rows_processed INTEGER,
    errors         INTEGER
);

<!-- Indexes for fast filtering & grouping -->
CREATE INDEX IF NOT EXISTS idx_sales_sale_date   ON sales (sale_date);
CREATE INDEX IF NOT EXISTS idx_sales_product_id  ON sales (product_id);
CREATE INDEX IF NOT EXISTS idx_sales_region      ON sales (region);