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

print("--- Sales Data Cube Report Configuration ---")
group_by_region = input("Include Region in report? (y/n): ").strip().lower() == 'y'
group_by_product = input("Include Product in report? (y/n): ").strip().lower() == 'y'
group_by_quarter = input("Group by Quarter? (y/n): ").strip().lower() == 'y'
metric = input("Metric to show (sold/revenue): ").strip().lower()

if metric not in ["sold", "revenue"]:
    print("Invalid metric. ")
    metric = "sold"

columns = []
grouping_elements = []

if group_by_region:
    columns.append("g.region_name AS region")
    grouping_elements.append("g.region_name")

if group_by_quarter:
    columns.extend([
        "EXTRACT(YEAR FROM d.full_date) AS year",
        "EXTRACT(QUARTER FROM d.full_date) AS quarter"
    ])
    grouping_elements.extend([
        "EXTRACT(YEAR FROM d.full_date)",
        "EXTRACT(QUARTER FROM d.full_date)"
    ])

if group_by_product:
    columns.append("p.article_name AS product")
    grouping_elements.append("p.article_name")

columns.append(f"SUM(f.{metric}) AS total_{metric}")

grouping_sets = []

if grouping_elements:
    grouping_sets.append(f"({', '.join(grouping_elements)})")
    if len(grouping_elements) > 1:
        grouping_sets.append(f"({', '.join(grouping_elements[:-1])})")
    grouping_sets.append("()")
else:
    grouping_sets.append("()")

query = f"""
    SELECT
        {', '.join(columns)}
    FROM fact_sales f
    JOIN dim_date d ON f.date_id = d.date_id
    JOIN dim_geo g ON f.geo_id = g.geo_id
    JOIN dim_product p ON f.product_id = p.product_id
    GROUP BY GROUPING SETS (
        {', '.join(grouping_sets)}
    )
    ORDER BY {', '.join([col.split(' AS ')[-1] for col in columns if ' AS ' in col])};
"""

cursor.execute(query)
rows = cursor.fetchall()
colnames = [desc[0] for desc in cursor.description]
df = pd.DataFrame(rows, columns=colnames)


if 'year' in df.columns and 'quarter' in df.columns:
    df["period"] = df.apply(
        lambda row: f"quarter {int(row['quarter'])}, {int(row['year'])}"
        if pd.notnull(row['year']) and pd.notnull(row['quarter'])
        else None,
        axis=1
    )


pivot_index = []
if group_by_region:
    pivot_index.append("region")
if "period" in df.columns:
    pivot_index.append("period")

pivot = pd.pivot_table(
    df,
    index=pivot_index if pivot_index else None,
    columns="product" if group_by_product else None,
    values=f"total_{metric}",
    aggfunc="sum",
    fill_value=0,
    margins=True,
    margins_name="total"
)


pd.set_option("display.max_columns", None)
print("\n--- Report Output ---")
print(pivot)

cursor.close()
conn.close()
