import pandas as pd
import psycopg2

conn = psycopg2.connect(
    database="parser_db",
    user="macbookpro",
    host="localhost",
    port=5432
)

df = pd.read_sql("SELECT * FROM real_estate3", conn)

# очистка
df = df.drop_duplicates(subset=["link"])

# фильтр (пример)
df = df[df["location"].notna()]

# сортировка
df = df.sort_values(by="id", ascending=False)

# экспорт
df.to_excel("real_estate.xlsx", index=False)

print("DONE")