from src.generate_data import build_stores_csv
from src.generate_data import build_products_csv
from src.generate_data import build_sales_csv
from src.pipeline import build_dim_date, build_dim_product, build_dim_store, build_fact_sales
from src.pipeline import load_clean_sales_dataset, load_sales_csv

if __name__ == "__main__":
	print(build_products_csv())
	print(build_stores_csv())
	sales_path = build_sales_csv()
	print(sales_path)
	load_sales_csv(sales_path)
	sales, products, stores, issues = load_clean_sales_dataset()
	dim_date = build_dim_date(sales)
	dim_product = build_dim_product(products)
	dim_store = build_dim_store(stores)