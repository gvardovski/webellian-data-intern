from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


PRODUCTS = [
	("P001", "Wireless Mouse", "Electronics", 79.09),
	("P002", "Mechanical Keyboard", "Electronics", 99.19),
	("P003", "USB-C Hub", "Electronics", 39.99),
	("P004", "Noise Cancelling Headphones", "Electronics", 149.29),
	("P005", "Smartwatch", "Electronics", 199.39),
	("P006", "Espresso Beans", "Grocery", 12.49),
	("P007", "Olive Oil", "Grocery", 14.59),
	("P008", "Granola", "Grocery", 6.69),
	("P009", "Pasta", "Grocery", 3.79),
	("P010", "Green Tea", "Grocery", 7.89),
	("P011", "T-Shirt", "Clothing", 19.99),
	("P012", "Denim Jeans", "Clothing", 49.09),
	("P013", "Hoodie", "Clothing", 39.19),
	("P014", "Sneakers", "Clothing", 69.29),
	("P015", "Baseball Cap", "Clothing", 12.39),
	("P016", "Desk Lamp", "Home", 29.49),
	("P017", "Ceramic Mug", "Home", 9.59),
	("P018", "Throw Blanket", "Home", 34.69),
	("P019", "Yoga Mat", "Fitness", 24.79),
	("P020", "Water Bottle", "Fitness", 14.89),
	("P021", "Notebook", "Stationery", 4.99),
	("P022", "Ballpoint Pens", "Stationery", 2.09),
]

STORES = [
	("S001", "Central Mart", "Warsaw"),
	("S002", "Urban Store", "Krakow"),
	("S003", "City Retail", "Gdansk"),
	("S004", "Metro Point", "Wroclaw"),
	("S005", "Corner Shop", "Warsaw"),
	("S006", "River Market", "Krakow"),
]

PRODUCT_CATEGORY_BY_ID = {product_id: category for product_id, _, category, _ in PRODUCTS}
PRODUCT_PRICE_BY_ID = {product_id: price for product_id, _, _, price in PRODUCTS}


def build_products_csv(output_dir: Path | None = None) -> Path:

	base_dir = output_dir or Path(__file__).resolve().parents[1] / "data"
	base_dir.mkdir(parents=True, exist_ok=True)

	output_path = base_dir / "products.csv"
	with output_path.open("w", newline="", encoding="utf-8") as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow(["product_id", "product_name", "category", "price"])
		writer.writerows(PRODUCTS)

	return output_path


def build_stores_csv(output_dir: Path | None = None) -> Path:
	base_dir = output_dir or Path(__file__).resolve().parents[1] / "data"
	base_dir.mkdir(parents=True, exist_ok=True)

	output_path = base_dir / "stores.csv"
	with output_path.open("w", newline="", encoding="utf-8") as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow(["store_id", "store_name", "city"])
		writer.writerows(STORES)

	return output_path


def build_sales_csv(output_dir: Path | None = None, row_count: int = 840, day_count: int = 21) -> Path:
	base_dir = output_dir or Path(__file__).resolve().parents[1] / "data"
	base_dir.mkdir(parents=True, exist_ok=True)

	random_generator = random.Random(42)
	product_ids = [p[0] for p in PRODUCTS]
	store_ids = [store_id for store_id, _, _ in STORES]
	start_time = datetime(2025, 5, 1, 8, 0, 0)

	output_path = base_dir / "sales.csv"
	with output_path.open("w", newline="", encoding="utf-8") as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow(["sale_id", "product_id", "store_id", "quantity", "price", "timestamp"])

		for index in range(row_count):
			product_id = random_generator.choice(product_ids)
			store_id = random_generator.choice(store_ids)
			quantity = random_generator.randint(-1, 77)
			base_price = PRODUCT_PRICE_BY_ID[product_id]
			price = round(base_price * quantity, 2)
			day_offset = index % day_count
			timestamp = start_time + timedelta(
				days=day_offset,
				hours=random_generator.randint(0, 11),
				minutes=random_generator.randint(0, 59),
			)
			writer.writerow([
				index + 1,
				product_id,
				store_id,
				quantity,
				f"{price:.2f}",
				timestamp.strftime("%Y-%m-%d %H:%M:%S"),
			])

	return output_path