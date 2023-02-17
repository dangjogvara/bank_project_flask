import os

import psycopg2
from flask import Flask, render_template, url_for
from db import DBConnect
from dotenv import load_dotenv

# load .env file
load_dotenv()
app = Flask(__name__)

# load database config
user = os.environ.get('USER')
password = os.environ.get('PASSWORD')
host = os.environ.get('HOST')
database = os.environ.get('database')
port = os.environ.get('PORT')

# db cursor
conn = DBConnect.get_connection(user, password, host, database, port)


@app.route('/')
def index():
    return render_template('index.html', title='Dangjogvara Bank', url_for=url_for)


@app.route('/customer')
def customer():
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM student')
        student_list = cursor.fetchall()
        return render_template('customers.html', student_list=student_list, url_for=url_for)
    except(Exception, psycopg2.Error) as e:
        return f'Could not fetch students.\nError: {e}'
    finally:
        cursor.close()


@app.route('/customer/<user_id>')
def customer_account(user_id):
    cursor.execute('SELECT * FROM student WHERE customer_id=%s', user_id)
    student_list = cursor.fetchall()
    return render_template('account.html', user_id=user_id, student_list=student_list, url_for=url_for)


if __name__ == '__main__':
    app.run(debug=True)
