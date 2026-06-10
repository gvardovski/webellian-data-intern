from __future__ import annotations

from pathlib import Path
from typing import Mapping

import pandas as pd


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
