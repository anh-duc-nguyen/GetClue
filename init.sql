CREATE TABLE IF NOT EXISTS sales (
  order_id   BIGINT      PRIMARY KEY,
  sale_date  DATE        NOT NULL,
  product_id TEXT        NOT NULL,
  region     TEXT        NOT NULL,
  quantity   INTEGER     NOT NULL,
  unit_price NUMERIC(10,2) NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_sales_sale_date   ON sales (sale_date);
CREATE INDEX IF NOT EXISTS idx_sales_product_id  ON sales (product_id);
CREATE INDEX IF NOT EXISTS idx_sales_region      ON sales (region);
