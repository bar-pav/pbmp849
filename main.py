from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import json


app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        database='flask_db',
        user="postgres",
        password="1234",
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
        cur.execute("INSERT INTO form_data (data) VALUES (%s);", (json.dumps(form_data),))
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
        cur.execute('SELECT * FROM form_data;')
        data = cur.fetchall()
        print(data)
        return render_template('list.html', dataset=data)
    except Exception as e:
        raise e
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    app.run(debug=True)