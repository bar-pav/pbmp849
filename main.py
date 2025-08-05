import json
from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import config

app = Flask(__name__)


app.config['POSTGRES_HOST'] = config.POSTGRES_HOST
app.config['POSTGRES_USER'] = config.POSTGRES_USER
app.config['POSTGRES_PASSWORD'] = config.POSTGRES_PASSWORD
app.config['POSTGRES_DB_NAME'] = config.POSTGRES_DB_NAME
app.config['POSTGRES_FLASK_TABLE'] = 'flask_table'


def get_db_connection(database=None):
    conn = psycopg2.connect(
        host=app.config['POSTGRES_HOST'],
        database=database or app.config['POSTGRES_DB_NAME'],
        user=app.config['POSTGRES_USER'],
        password=app.config['POSTGRES_PASSWORD'],
    )
    return conn

@app.route("/")
def main_page():
    return render_template("main.html")

@app.route("/form-submit/", methods=['POST'])
def form_submit():
    print(request.form.to_dict())
    form_data = request.form.to_dict()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO flask_table (data) VALUES (%s);", (json.dumps(form_data),))
        conn.commit()
        # return redirect(url_for('view_data'))
        return {'status': 'OK', 'redirectURL': url_for('view_data')}
    except Exception as e:
        raise e
    finally:
        cur.close()
        conn.close()

@app.route("/list/")
def view_data():
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute('SELECT * FROM flask_table;')
        data = cur.fetchall()
        print(data)
        return render_template('list.html', dataset=data)
    except Exception as e:
        raise e
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0')