# import pandas as pd
# import psycopg2

# conn = psycopg2.connect(
#     database="parser_db",
#     user="macbookpro",
#     host="localhost",
#     port=5432
# )

# df = pd.read_sql("SELECT * FROM real_estate3", conn)

# # очистка
# df = df.drop_duplicates(subset=["link"])

# # фильтр (пример)
# df = df[df["location"].notna()]

# # сортировка
# df = df.sort_values(by="id", ascending=False)

# # экспорт
# df.to_excel("real_estate.xlsx", index=False)

# print("DONE")


import pandas as pd
import psycopg2
from datetime import datetime

conn = psycopg2.connect(
    database="parser_db",
    user="macbookpro",
    host="localhost",
    port=5432
)

query = """
SELECT *
FROM real_estate3
WHERE created_at >= CURRENT_DATE
  AND created_at < CURRENT_DATE + INTERVAL '1 day'
  AND phone IN (
      SELECT phone
      FROM real_estate3
      WHERE phone IS NOT NULL
        AND phone <> ''
      GROUP BY phone
      HAVING COUNT(*) = 1
  )
"""

df = pd.read_sql(query, conn)

conn.close()

# убрать дубли по ссылке (на всякий случай)
df = df.drop_duplicates(subset=["link"])

# убрать записи без города
df = df[df["location"].notna()]

# последние объявления сверху
df = df.sort_values(by="id", ascending=False)

# имя файла по текущей дате
filename = datetime.now().strftime("%d.%m.%Y.xlsx")

# экспорт
df.to_excel(filename, index=False)

print(f"Exported {len(df)} records to {filename}.")