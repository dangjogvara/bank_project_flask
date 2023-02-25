import os
import psycopg2
from flask import Flask, render_template, url_for
from db import DBConnect
from dotenv import load_dotenv

# load .env file
app = Flask(__name__)
load_dotenv()

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


@app.route('/client')
def client():
    cursor = conn.cursor()
    try:
        cursor.execute("""SELECT c.client_id, c.first_name, c.middle_name, c.last_name, c.email, c.phone_number,
        a.account_number, a.balance
        FROM client c, account a
        WHERE c.client_id = a.client_id""")

        client_list = cursor.fetchall()
        return render_template('clients.html', client_list=client_list, url_for=url_for)
    except (Exception, psycopg2.Error) as e:
        return f'Could not fetch clients.\nError: {e}'
    finally:
        cursor.close()


@app.route('/client/<user_id>')
def client_account(user_id):
    cursor = conn.cursor()
    try:
        cursor.execute("""SELECT c.client_id, c.first_name, c.middle_name, c.last_name, c.email, c.phone_number, 
        a.account_number, a.balance
        FROM client c, account a
        WHERE c.client_id = a.client_id and c.client_id=%s""", user_id)

        my_account = cursor.fetchall()
        return render_template('account.html', my_account=my_account, url_for=url_for)
    except (Exception, psycopg2.Error) as e:
        return f'Could not fetch account.\nError: {e}'
    finally:
        cursor.close()


if __name__ == '__main__':
    app.run(debug=True)
