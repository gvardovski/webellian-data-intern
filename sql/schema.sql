CREATE TABLE dim_product (
	product_id VARCHAR PRIMARY KEY,
	product_name VARCHAR,
	category VARCHAR
);

CREATE TABLE dim_store (
	store_id VARCHAR PRIMARY KEY,
	store_name VARCHAR,
	city VARCHAR
);

CREATE TABLE dim_date (
	date_id DATE PRIMARY KEY,
	year INTEGER,
	month INTEGER,
	day INTEGER,
	weekday VARCHAR
);

CREATE TABLE fact_sales (
	sale_id INTEGER PRIMARY KEY,
	product_id VARCHAR,
	store_id VARCHAR,
	date_id DATE,
	quantity INTEGER,
	price DECIMAL(10,2),
	total_sale DECIMAL(10,2),
	FOREIGN KEY(product_id)
		REFERENCES dim_product(product_id),
	FOREIGN KEY(store_id)
		REFERENCES dim_store(store_id),
	FOREIGN KEY(date_id)
		REFERENCES dim_date(date_id)
);
