import psycopg2
import pandas as pd

try:
    conn = psycopg2.connect(
        dbname="exercise_6", 
        user="postgres", 
        password="postgres", 
        host="localhost", 
        port= "5432"
    )
    cursor = conn.cursor()
except Exception as e:
    print("Connection failed:", e)
    exit(1)

print("Creating star schema tables...")
with open("../sql/star_schema.sql", "r") as f:
    schema_sql = f.read()
try:
    cursor.execute(schema_sql)
    conn.commit()
    print("Star schema created successfully.")
except Exception as e:
    print("Schema execution failed:", e)
    conn.rollback()

print("Loading CSV data...")
df = pd.read_csv("../data/sales.csv", sep=';', encoding='ISO-8859-1', on_bad_lines='skip')
df['Revenue'] = df['Revenue'].str.replace(',', '.').astype(float)
df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')
print(f"Data loaded successfully. Processing {len(df)} rows...")

def insert_dim_date(date):
    cursor.execute("SELECT date_id FROM dim_date WHERE full_date = %s", (date,))
    res = cursor.fetchone()
    if res:
        return res[0]
    cursor.execute(
        "INSERT INTO dim_date (full_date, day, month, quarter, year) VALUES (%s, %s, %s, %s, %s) RETURNING date_id",
        (date, date.day, date.month, (date.month-1)//3 + 1, date.year)
    )
    conn.commit()
    return cursor.fetchone()[0]

def insert_dim_geo(shop_name):
    cursor.execute("""
        SELECT s.ShopID, s.Name, c.Name, r.Name, co.Name
        FROM Shop s
        JOIN City c ON s.CityID = c.CityID
        JOIN Region r ON c.RegionID = r.RegionID
        JOIN Country co ON r.CountryID = co.CountryID
        WHERE s.Name = %s
    """, (shop_name,))
    result = cursor.fetchone()
    if not result:
        return None
    shop_id, shop, city, region, country = result

    cursor.execute("SELECT geo_id FROM dim_geo WHERE shop_id = %s", (shop_id,))
    res = cursor.fetchone()
    if res:
        return res[0]
    cursor.execute("""
        INSERT INTO dim_geo (shop_id, shop_name, city_dim_geoname, region_name, country_name)
        VALUES (%s, %s, %s, %s, %s) RETURNING geo_id
    """, (shop_id, shop, city, region, country))
    conn.commit()
    return cursor.fetchone()[0]

def insert_dim_product(article_name):
    cursor.execute("""
        SELECT a.ArticleID, a.Name, pg.Name, pf.Name, pc.Name
        FROM Article a
        JOIN ProductGroup pg ON a.ProductGroupID = pg.ProductGroupID
        JOIN ProductFamily pf ON pg.ProductFamilyID = pf.ProductFamilyID
        JOIN ProductCategory pc ON pf.ProductCategoryID = pc.ProductCategoryID
        WHERE a.Name = %s
    """, (article_name,))
    result = cursor.fetchone()
    if not result:
        return None
    article_id, art, group, family, category = result

    cursor.execute("SELECT product_id FROM dim_product WHERE article_id = %s", (article_id,))
    res = cursor.fetchone()
    if res:
        return res[0]
    cursor.execute("""
        INSERT INTO dim_product (article_id, article_name, product_group, product_family, product_category)
        VALUES (%s, %s, %s, %s, %s) RETURNING product_id
    """, (article_id, art, group, family, category))
    conn.commit()
    return cursor.fetchone()[0]

print("Starting ETL process...")
processed_count = 0
skipped_count = 0

for i, (_, row) in enumerate(df.iterrows()):
    if i % 100 == 0 and i > 0:  # Progress indicator every 100 rows
        print(f"Progress: {i}/{len(df)} rows processed ({processed_count} inserted, {skipped_count} skipped)")
    
    date_id = insert_dim_date(row['Date'])
    geo_id = insert_dim_geo(row['Shop'])
    product_id = insert_dim_product(row['Article'])
    
    if geo_id and product_id:
        cursor.execute("""
            INSERT INTO fact_sales (date_id, geo_id, product_id, sold, revenue)
            VALUES (%s, %s, %s, %s, %s)
        """, (date_id, geo_id, product_id, row['Sold'], row['Revenue']))
        processed_count += 1
    else:
        print(f"Skipping row {i}: Shop '{row['Shop']}' or Article '{row['Article']}' not found in operational database")
        skipped_count += 1

conn.commit()
print(f"ETL process completed!")
print(f"Total rows processed: {len(df)}")
print(f"Rows inserted into fact table: {processed_count}")
print(f"Rows skipped: {skipped_count}")

cursor.close()
conn.close()




