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
        cursor.execute("""SELECT c.first_name, c.middle_name, c.last_name, c.email, c.phone_number, 
        a.account_number, a.balance
        FROM customer c, account a
        WHERE c.customer_id = a.customer_id""")

        customer_list = cursor.fetchall()
        return render_template('customers.html', customer_list=customer_list, url_for=url_for)
    except(Exception, psycopg2.Error) as e:
        return f'Could not fetch students.\nError: {e}'
    finally:
        cursor.close()


@app.route('/customer/<user_id>')
def customer_account(user_id):
    cursor = conn.cursor()
    try:
        cursor.execute("""SELECT c.first_name, c.middle_name, c.last_name, c.email, c.phone_number, 
        a.account_number, a.balance
        FROM customer c, account a
        WHERE c.customer_id = a.customer_id and c.customer_id=%s""", user_id)
        
        my_account = cursor.fetchall()
        return render_template('account.html', my_account=my_account, url_for=url_for)
    except(Exception, psycopg2.Error) as e:
        return f'Could not fetch account.\nError: {e}'
    finally:
        cursor.close()


if __name__ == '__main__':
    app.run(debug=True)
