CREATE TABLE
    dim_date (
        date_id SERIAL PRIMARY KEY,
        full_date DATE NOT NULL,
        day INT,
        month INT,
        quarter INT,
        year INT
    );

CREATE TABLE
    dim_product (
        product_id SERIAL PRIMARY KEY,
        article_id INT UNIQUE,
        article_name VARCHAR(255),
        product_group VARCHAR(255),
        product_family VARCHAR(255),
        product_category VARCHAR(255)
    );

CREATE TABLE
    dim_geo (
        geo_id SERIAL PRIMARY KEY,
        shop_id INT UNIQUE,
        shop_name VARCHAR(255),
        city_name VARCHAR(255),
        region_name VARCHAR(255),
        country_name VARCHAR(255)
    );

CREATE TABLE
    fact_sales (
        sales_id SERIAL PRIMARY KEY,
        date_id INT REFERENCES dim_date (date_id),
        geo_id INT REFERENCES dim_geo (geo_id),
        product_id INT REFERENCES dim_product (product_id),
        sold INT NOT NULL,
        revenue NUMERIC(12, 2) NOT NULL
    );
