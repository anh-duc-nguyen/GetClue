# app.py
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import psycopg  # using v3
import os

DB_DSN = os.getenv(
    "DB_DSN",
    "postgresql://analytics_user:analytics_pass@postgres:5432/analytics" #TODO: Use .env
)

app = FastAPI(title="Analytics API")

class MonthlySummary(BaseModel):
    month: str   # YYYY-MM
    revenue: float

class TopProduct(BaseModel):
    product_id: str
    product_name: Optional[str]
    revenue: float

@app.on_event("startup")
def startup():
    app.state.db = psycopg.connect(DB_DSN)

@app.on_event("shutdown")
def shutdown():
    app.state.db.close()

@app.get("/sales/monthly", response_model=List[MonthlySummary])
def get_monthly_sales(
    product_id: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
):
    filters = []
    params = {}
    if product_id:
        filters.append("product_id = %(product_id)s")
        params["product_id"] = product_id
    if region:
        filters.append("region = %(region)s")
        params["region"] = region
    if start_date:
        filters.append("sale_date >= %(start_date)s")
        params["start_date"] = start_date
    if end_date:
        filters.append("sale_date <= %(end_date)s")
        params["end_date"] = end_date

    where = f"WHERE {' AND '.join(filters)}" if filters else ""
    sql = f"""
      SELECT to_char(sale_date, 'YYYY-MM') AS month,
             SUM(quantity * unit_price)::float AS revenue
      FROM sales
      {where}
      GROUP BY 1
      ORDER BY 1;
    """
    with app.state.db.cursor() as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()
    return [{"month": m, "revenue": r} for m, r in rows]


@app.get("/products/top5", response_model=List[TopProduct])
def get_top_products(
    region: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
):
    filters = []
    params = {}
    if region:
        filters.append("region = %(region)s")
        params["region"] = region
    if start_date:
        filters.append("sale_date >= %(start_date)s")
        params["start_date"] = start_date
    if end_date:
        filters.append("sale_date <= %(end_date)s")
        params["end_date"] = end_date

    where = f"WHERE {' AND '.join(filters)}" if filters else ""
    sql = f"""
      SELECT product_id,
             SUM(quantity * unit_price)::float AS revenue
      FROM sales
      {where}
      GROUP BY product_id
      ORDER BY revenue DESC
      LIMIT 5;
    """
    with app.state.db.cursor() as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()
    return [{"product_id": pid, "product_name": None, "revenue": rev} for pid, rev in rows]
