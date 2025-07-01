import psycopg2
import pandas as pd

conn = psycopg2.connect(
    dbname="exercise_6",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

query = """
    SELECT
        g.region_name AS region,
        EXTRACT(YEAR FROM d.full_date) AS year,
        EXTRACT(QUARTER FROM d.full_date) AS quarter,
        p.article_name AS product,
        SUM(f.sold) AS total_sold
    FROM fact_sales f
    JOIN dim_date d ON f.date_id = d.date_id
    JOIN dim_geo g ON f.geo_id = g.geo_id
    JOIN dim_product p ON f.product_id = p.product_id
    GROUP BY GROUPING SETS (
        (g.region_name, EXTRACT(YEAR FROM d.full_date), EXTRACT(QUARTER FROM d.full_date), p.article_name),
        (g.region_name, EXTRACT(YEAR FROM d.full_date), EXTRACT(QUARTER FROM d.full_date)),
        (p.article_name),
        ()
    )
    ORDER BY region, year, quarter, product;
"""

cursor.execute(query)
rows = cursor.fetchall()

df = pd.DataFrame(rows, columns=["region", "year", "quarter", "product", "total_sold"])

df["period"] = df.apply(
    lambda row: f"quarter {int(row['quarter'])}, {int(row['year'])}" if pd.notnull(row['year']) and pd.notnull(row['quarter']) else None,
    axis=1
)

pivot = pd.pivot_table(
    df,
    index=["region", "period"],
    columns="product",
    values="total_sold",
    aggfunc="sum",
    fill_value=0,
    margins=True,
    margins_name="total"
)

# Display result
pd.set_option("display.max_columns", None)
print(pivot)

# Clean up
cursor.close()
conn.close()