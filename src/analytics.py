from __future__ import annotations

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


TOP_PRODUCTS_BY_REVENUE_SQL = """
SELECT
    p.product_name,
    SUM(f.total_sale) AS revenue
FROM fact_sales f
JOIN dim_product p
ON f.product_id = p.product_id
GROUP BY p.product_name
ORDER BY revenue DESC
LIMIT {limit};
"""


def top_products_by_revenue(
	fact_sales: pd.DataFrame,
	dim_product: pd.DataFrame,
	limit: int = 10,
	output_dir: str | Path | None = None,
) -> pd.DataFrame:
	result = (
		fact_sales.merge(dim_product[["product_id", "product_name"]], on="product_id", how="inner")
		.groupby("product_name", as_index=False)["total_sale"]
		.sum()
		.rename(columns={"total_sale": "revenue"})
		.sort_values("revenue", ascending=False)
		.head(limit)
		.reset_index(drop=True)
	)

	base_dir = Path(output_dir) if output_dir is not None else Path(__file__).resolve().parents[1] / "output"
	base_dir.mkdir(parents=True, exist_ok=True)
	result.to_csv(base_dir / "top_products.csv", index=False)
	return result


def revenue_by_city(
	fact_sales: pd.DataFrame,
	dim_store: pd.DataFrame,
	output_dir: str | Path | None = None,
) -> pd.DataFrame:
	result = (
		fact_sales.merge(dim_store[["store_id", "city"]], on="store_id", how="inner")
		.groupby("city", as_index=False)["total_sale"]
		.sum()
		.rename(columns={"total_sale": "revenue"})
		.sort_values("revenue", ascending=False)
		.reset_index(drop=True)
	)

	base_dir = Path(output_dir) if output_dir is not None else Path(__file__).resolve().parents[1] / "output"
	base_dir.mkdir(parents=True, exist_ok=True)
	result.to_csv(base_dir / "revenue_by_city.csv", index=False)
	return result


def daily_sales_trend(
	fact_sales: pd.DataFrame,
	output_dir: str | Path | None = None,
) -> pd.DataFrame:
	trend = (
		fact_sales.assign(date_id=pd.to_datetime(fact_sales["date_id"]))
		.groupby("date_id", as_index=False)["total_sale"]
		.sum()
		.rename(columns={"total_sale": "revenue"})
		.sort_values("date_id")
		.reset_index(drop=True)
	)

	base_dir = Path(output_dir) if output_dir is not None else Path(__file__).resolve().parents[1] / "output"
	base_dir.mkdir(parents=True, exist_ok=True)

	figure, axis = plt.subplots(figsize=(10, 5))
	axis.plot(trend["date_id"], trend["revenue"], marker="o")
	axis.set_title("Daily Sales Trend")
	axis.set_xlabel("Date")
	axis.set_ylabel("Revenue")
	axis.grid(True, alpha=0.3)
	figure.autofmt_xdate()
	figure.tight_layout()
	figure.savefig(base_dir / "daily_sales_trend.png")
	plt.close(figure)

	return trend