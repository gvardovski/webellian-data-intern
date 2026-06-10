from src.generate_data import build_stores_csv
from src.generate_data import build_products_csv
from src.generate_data import build_sales_csv


if __name__ == "__main__":
	print(build_products_csv())
	print(build_stores_csv())
	print(build_sales_csv())
	