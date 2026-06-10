from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


PRODUCTS = [
	("P001", "Wireless Mouse", "Electronics"),
	("P002", "Mechanical Keyboard", "Electronics"),
	("P003", "USB-C Hub", "Electronics"),
	("P004", "Noise Cancelling Headphones", "Electronics"),
	("P005", "Smartwatch", "Electronics"),
	("P006", "Espresso Beans", "Grocery"),
	("P007", "Olive Oil", "Grocery"),
	("P008", "Granola", "Grocery"),
	("P009", "Pasta", "Grocery"),
	("P010", "Green Tea", "Grocery"),
	("P011", "T-Shirt", "Clothing"),
	("P012", "Denim Jeans", "Clothing"),
	("P013", "Hoodie", "Clothing"),
	("P014", "Sneakers", "Clothing"),
	("P015", "Baseball Cap", "Clothing"),
	("P016", "Desk Lamp", "Home"),
	("P017", "Ceramic Mug", "Home"),
	("P018", "Throw Blanket", "Home"),
	("P019", "Yoga Mat", "Fitness"),
	("P020", "Water Bottle", "Fitness"),
	("P021", "Notebook", "Stationery"),
	("P022", "Ballpoint Pens", "Stationery"),
]

STORES = [
	("S001", "Central Mart", "Warsaw"),
	("S002", "Urban Store", "Krakow"),
	("S003", "City Retail", "Gdansk"),
	("S004", "Metro Point", "Wroclaw"),
	("S005", "Corner Shop", "Warsaw"),
	("S006", "River Market", "Krakow"),
]

PRODUCT_CATEGORY_BY_ID = {product_id: category for product_id, _, category in PRODUCTS}
BASE_PRICE_BY_CATEGORY = {
	"Electronics": 79.99,
	"Grocery": 9.99,
	"Clothing": 29.99,
	"Home": 24.99,
	"Fitness": 19.99,
	"Stationery": 4.99,
}


def build_products_csv(output_dir: Path | None = None) -> Path:

	base_dir = output_dir or Path(__file__).resolve().parents[1] / "data"
	base_dir.mkdir(parents=True, exist_ok=True)

	output_path = base_dir / "products.csv"
	with output_path.open("w", newline="", encoding="utf-8") as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow(["product_id", "product_name", "category"])
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
	product_ids = [product_id for product_id, _, _ in PRODUCTS]
	store_ids = [store_id for store_id, _, _ in STORES]
	start_time = datetime(2025, 5, 1, 8, 0, 0)

	output_path = base_dir / "sales.csv"
	with output_path.open("w", newline="", encoding="utf-8") as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow(["sale_id", "product_id", "store_id", "quantity", "price", "timestamp"])

		for index in range(row_count):
			product_id = random_generator.choice(product_ids)
			store_id = random_generator.choice(store_ids)
			quantity = random_generator.randint(1, 5)
			category = PRODUCT_CATEGORY_BY_ID[product_id]
			base_price = BASE_PRICE_BY_CATEGORY[category]
			price = round(base_price * random_generator.uniform(0.85, 1.15), 2)
			day_offset = index % day_count
			timestamp = start_time + timedelta(
				days=day_offset,
				hours=random_generator.randint(0, 11),
				minutes=random_generator.randint(0, 59),
			)
			writer.writerow([
				f"SA{index + 1:04d}",
				product_id,
				store_id,
				quantity,
				f"{price:.2f}",
				timestamp.strftime("%Y-%m-%d %H:%M:%S"),
			])

	return output_path