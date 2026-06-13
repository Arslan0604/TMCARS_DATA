import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="parser_db",
    user="macbookpro"
)

cur = conn.cursor()

cur.execute("SELECT current_database();")
print(cur.fetchone())

conn.close()