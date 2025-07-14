import pandas as pd

df = pd.read_csv("./data/sales.csv", sep=';', encoding='ISO-8859-1', on_bad_lines='skip')
print(df.head(20))
