import psycopg2


conn = psycopg2.connect(
    host='localhost',
    database='flask_db',
    user="postgres",
    password="1234",
)

cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS form_data')
cursor.execute('CREATE TABLE form_data (id serial PRIMARY KEY,'
'                                       data jsonb)')


conn.commit()
cursor.close()
conn.close()