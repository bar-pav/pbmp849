import psycopg2
from main import app, get_db_connection

try:
    conn = get_db_connection(database='postgres')
    print(conn)
    cursor = conn.cursor()
    conn.autocommit = True
    print(cursor)
    cursor.execute("SELECT * FROM pg_database WHERE datname='{}';".format(app.config['POSTGRES_DB_NAME']))
    exist_db = cursor.fetchone()
    print(exist_db)
    if not exist_db:
        cursor.execute("CREATE DATABASE {};".format(app.config['POSTGRES_DB_NAME']))
        conn.commit()
except Exception as e:
    print('БД не создана.')
finally:
    cursor.close()
    conn.close()


try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM information_schema.tables WHERE table_name='{}';".format(app.config['POSTGRES_FLASK_TABLE']))
    exist_table = cursor.fetchone()
    if not exist_table:
        cursor.execute('CREATE TABLE "{}" (id serial PRIMARY KEY,'
                       '                                       data jsonb);'.format(app.config['POSTGRES_FLASK_TABLE']))
        conn.commit()
except Exception as e:
    print('Таблица не создана')

finally:
    cursor.close()
    conn.close()
# cursor.execute('DROP TABLE IF EXISTS form_data')
