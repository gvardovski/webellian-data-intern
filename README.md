# Webellian

A small synthetic retail analytics project that generates CSV data, builds a star schema, and produces simple analytics outputs.

## What it creates

- `data/products.csv`
- `data/stores.csv`
- `data/sales.csv`
- `output/top_products.csv`
- `output/revenue_by_city.csv`
- `output/daily_sales_trend.png`

## Project Structure

- `main.py` - entry point that runs the full pipeline
- `src/generate_data.py` - builds the synthetic CSV inputs
- `src/pipeline.py` - loads, validates, cleans, and shapes the data
- `src/analytics.py` - generates report tables and chart output
- `sql/schema.sql` - star schema definition

## Install Dependencies

```bash
poetry install
```

## Run

```bash
poetry run python main.py
```

## Notes

- The analytics helpers write their outputs to the `output/` directory by default.
- The pipeline uses pandas for data loading and transformation.
- The sales data is synthetic and generated deterministically.
