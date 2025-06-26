# GetClue Analytics API

This project provides a simple analytics API built with FastAPI and PostgreSQL, along with a CSV ingestion script (`ingest.py`) and a sample data generator (`generate_sample.py`).

## Prerequisites

- **Docker** & **Docker Compose** installed
- **Python 3.8+** (for running local scripts)

## Setup & Run

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-dir>
   ```

2. **Start services with Docker Compose**
   ```bash
   docker-compose build
   docker-compose up -d
   ```
   - **Postgres** will be available at `postgresql://analytics_user:analytics_pass@localhost:5432/analytics`
   - **FastAPI** will be running at `http://localhost:8000`
   Visit `http://localhost:8000` to view the app.


3. **Initialize database schema**
   - The `init.sql` file (mounted into Postgres) automatically creates the `sales` table and indexes on startup.

## Ingest CSV Data

### Manual via Script

1. **Copy `ingest.py` into the API container** (optional):
   ```bash
   docker cp ingest.py getclue-api-1:/app/ingest.py
   ```
2. **Run ingestion**
   ```bash
   docker exec -it getclue-api-1 python ingest.py path/to/your.csv
   ```
   Example with generated sample:
   ```bash
   docker exec -it getclue-api-1 python ingest.py sample_20250101_20250107.csv
   ```
   This will print the number of rows inserted.

### HTTP Upload Endpoint

You can also upload a CSV file via the FastAPI endpoint:

```bash
curl -X POST "http://localhost:8000/upload_csv" \
     -F "file=@path/to/your.csv"
```

- On success, returns a confirmation message.
- On failure, returns an HTTP 500 with error details.

## Generate Sample CSV

To quickly create a sample CSV, use the provided script:

```bash
python generate_sample.py
```

- Prompts for **start date** and **end date** in `YYYYMMDD` format.
- Generates one record per product per day between the dates.
- Outputs `sample_<start>_<end>.csv` in the current directory.

## API Endpoints

- **GET /**  
  Serves the homepage (HTML).

- **GET /sales/monthly**  
  Returns monthly revenue summaries.  
  **Query params**: `product_id`, `region`, `start_date`, `end_date` (optional).

- **GET /products/top5**  
  Returns top 5 products by revenue.  
  **Query params**: `region`, `start_date`, `end_date` (optional).

All endpoints return JSON responses.

---

Feel free to customize environment variables, add authentication, or extend the schema as needed.
