from __future__ import annotations

import logging
from pathlib import Path
from typing import Mapping

import pandas as pd


LOGGER = logging.getLogger(__name__)

EXPECTED_SALES_SCHEMA = {
	"sale_id": "int64",
	"product_id": "str",
	"store_id": "str",
	"quantity": "int64",
	"price": "float64",
	"timestamp": "str",
}


def load_csv(csv_path: str | Path) -> pd.DataFrame:
	return pd.read_csv(csv_path)


def validate_schema(dataframe: pd.DataFrame, expected_schema: Mapping[str, str]) -> None:
	for column_name, expected_dtype in expected_schema.items():
		assert column_name in dataframe.columns, f"Missing required column: {column_name}"
		actual_dtype = dataframe[column_name].dtype
		assert actual_dtype == expected_dtype, (
			f"Column {column_name} has dtype {actual_dtype}, expected {expected_dtype}"
		)


def load_sales_csv(csv_path: str | Path | None = None, validate: bool = True) -> pd.DataFrame:
	path = csv_path or Path(__file__).resolve().parents[1] / "data" / "sales.csv"
	sales = load_csv(path)

	if validate:
		validate_schema(sales, EXPECTED_SALES_SCHEMA)

	return sales


def validate_sales_data(
	sales: pd.DataFrame,
	products: pd.DataFrame,
	stores: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
	missing_values = sales[sales.isna().any(axis=1)]
	invalid_foreign_keys = sales[
		~sales["product_id"].isin(products["product_id"])
		| ~sales["store_id"].isin(stores["store_id"])
	]
	negative_quantity = sales[sales["quantity"] <= 0]
	negative_price = sales[sales["price"] <= 0]
	timestamp_values = pd.to_datetime(sales["timestamp"], errors="coerce")
	malformed_timestamps = sales[timestamp_values.isna()]

	LOGGER.warning("sales missing values rows: %d", len(missing_values))
	LOGGER.warning("sales invalid foreign key rows: %d", len(invalid_foreign_keys))
	LOGGER.warning("sales negative quantity rows: %d", len(negative_quantity))
	LOGGER.warning("sales negative price rows: %d", len(negative_price))
	LOGGER.warning("sales malformed timestamp rows: %d", len(malformed_timestamps))

	return {
		"missing_values": missing_values,
		"invalid_foreign_keys": invalid_foreign_keys,
		"negative_quantity": negative_quantity,
		"negative_price": negative_price,
		"malformed_timestamps": malformed_timestamps,
	}


def clean_sales_data(
	sales: pd.DataFrame,
	products: pd.DataFrame,
	stores: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
	sales = sales.copy()
	products = products.copy()
	stores = stores.copy()

	sales["timestamp"] = pd.to_datetime(sales["timestamp"], errors="coerce")
	sales = sales.dropna(subset=["timestamp"])
	sales = sales[(sales["quantity"] > 0) & (sales["price"] > 0)]
	sales["total_sale"] = round(sales["quantity"] * sales["price"], 2)

	products["category"] = products["category"].str.strip().str.title()
	stores["city"] = stores["city"].str.strip().str.title()

	return sales, products, stores


def load_clean_sales_dataset(
	data_dir: str | Path | None = None,
	validate_schema_first: bool = True,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, pd.DataFrame]]:
	base_dir = Path(data_dir) if data_dir is not None else Path(__file__).resolve().parents[1] / "data"
	sales = load_csv(base_dir / "sales.csv")
	products = load_csv(base_dir / "products.csv")
	stores = load_csv(base_dir / "stores.csv")

	if validate_schema_first:
		validate_schema(sales, EXPECTED_SALES_SCHEMA)

	issues = validate_sales_data(sales, products, stores)
	sales, products, stores = clean_sales_data(sales, products, stores)
	return sales, products, stores, issues
