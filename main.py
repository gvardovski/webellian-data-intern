from src.generate_data import build_stores_csv
from src.generate_data import build_products_csv
from src.generate_data import build_sales_csv
from src.pipeline import load_sales_csv
from src.pipeline import load_clean_sales_dataset

if __name__ == "__main__":
	print(build_products_csv())
	print(build_stores_csv())
	sales_path = build_sales_csv()
	print(sales_path)
	load_sales_csv(sales_path)
	sales, products, stores, issues = load_clean_sales_dataset()