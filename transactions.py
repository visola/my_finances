import mysql.connector
from config import *
from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def list_transactions():
    cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                host=MYSQL_HOST,
                                database=MYSQL_DATABASE)
    cursor = cnx.cursor()
    cursor.execute("select * from transactions")
    all_transactions = []
    for row in cursor:
        all_transactions.append({"id": row[0], "description": row[1]})
    print(all_transactions)
    cnx.close() 
    return render_template("transactions.html", transactions=all_transactions)

