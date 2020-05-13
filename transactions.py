import mysql.connector
from config import *
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
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

@app.route('/new')
def new_transaction():
    return render_template("transaction.html")

@app.route('/<id>')
def edit_transaction(id):
    print(id)
    cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                host=MYSQL_HOST,
                                database=MYSQL_DATABASE)
    cursor = cnx.cursor()
    select_transaction = ("select * from transactions where id=%s")
    transaction_data = (int(id),)
    cursor.execute(select_transaction, transaction_data)
    row = cursor.fetchone()
    cnx.close()
    return render_template("transaction.html", id=row[0], description=row[1])
    
@app.route('/save',methods=["POST"])
def save_transactions():
    cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                host=MYSQL_HOST,
                                database=MYSQL_DATABASE)
    cursor = cnx.cursor()
    if request.form["id"] != "": 
        update_transaction = ("update transactions set description=%s where id=%s")
        transaction_data = (request.form["description"],request.form["id"])
        cursor.execute(update_transaction, transaction_data)
    else:
        insert_transaction = ("insert into transactions(description) values(%s)")
        transaction_data = (request.form["description"],)
        cursor.execute(insert_transaction, transaction_data)
    cnx.commit()
    cnx.close()
    print(request.form["description"])
    return redirect(url_for("list_transactions"))


