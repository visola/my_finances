import mysql.connector
from config import *
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import session
from functools import wraps
import hashlib

app = Flask(__name__)

app.secret_key = MSQL_SECRET_KEY

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' in session:
           return f(*args, **kwargs)
        return redirect(url_for("get_login"))
    return decorated_function

@app.route('/transactions')
@login_required
def list_transactions():
    cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                host=MYSQL_HOST,
                                database=MYSQL_DATABASE)
    cursor = cnx.cursor()
    select_transactions = ("select * from transactions where user_id=%s")
    session_id_data = (session["id"],)
    cursor.execute(select_transactions,session_id_data)
    all_transactions = []
    for row in cursor:
        all_transactions.append({"id": row[0], "description": row[1]})
    cnx.close() 
    return render_template("transactions/index.html", transactions=all_transactions)

@app.route('/transactions/new')
@login_required
def new_transaction():
    return render_template("transactions/edit.html")

@app.route('/transactions/<id>')
@login_required
def edit_transaction(id):
    cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                host=MYSQL_HOST,
                                database=MYSQL_DATABASE)
    cursor = cnx.cursor()
    select_transaction = ("select * from transactions where id=%s and user_id=%s")
    transaction_data = (int(id),session["id"])
    cursor.execute(select_transaction, transaction_data)
    row = cursor.fetchone()
    cnx.close()
    if row is None :
        return "Page not found."
    return render_template("transactions/edit.html", id=row[0], description=row[1])
    
@app.route('/transactions/save',methods=["POST"])
@login_required
def save_transactions():
    cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                host=MYSQL_HOST,
                                database=MYSQL_DATABASE)
    cursor = cnx.cursor()
    if request.form["id"] != "": 
        update_transaction = ("update transactions set description=%s where id=%s and user_id = %s")
        transaction_data = (request.form["description"],request.form["id"],session["id"])
        cursor.execute(update_transaction, transaction_data)
    else:
        insert_transaction = ("insert into transactions(description,user_id) values(%s,%s)")
        transaction_data = (request.form["description"],session["id"])
        cursor.execute(insert_transaction, transaction_data)
    cnx.commit()
    cnx.close()
    if cursor.rowcount == 0:
        return "Sorry, there was an error."
    return redirect(url_for("list_transactions"))

@app.route('/users/new')
def create_user():
    return render_template("users/edit.html")

@app.route('/users/save',methods=["POST"])
def save_users():
    cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                host=MYSQL_HOST,
                                database=MYSQL_DATABASE)
    cursor = cnx.cursor()
    select_usuarios = ("select count(1) from usuarios where email=%s")
    email_data = (request.form["email"],)
    cursor.execute(select_usuarios, email_data)
    row = cursor.fetchone()
    if row[0] > 0:
        cnx.close()
        return redirect(url_for("create_user"))
    insert_transaction = ("insert into usuarios(name,email,senha) values(%s,%s,%s)")
    senha= hashlib.sha256(request.form["senha"].encode("utf-8")).hexdigest()
    transaction_data = (request.form["nome"],request.form["email"],senha)
    cursor.execute(insert_transaction, transaction_data)
    cnx.commit()
    cnx.close()
    return redirect(url_for("list_transactions"))

@app.route('/login',methods=["GET"])
def get_login():
    return render_template("login/index.html")

@app.route('/login',methods=["POST"])
def login():
    cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                host=MYSQL_HOST,
                                database=MYSQL_DATABASE)
    cursor = cnx.cursor()
    select_usuarios = ("select id from usuarios where email=%s and senha=%s")
    senha= hashlib.sha256(request.form["senha"].encode("utf-8")).hexdigest()
    email_data = (request.form["email"],senha)
    cursor.execute(select_usuarios, email_data)
    row = cursor.fetchone()
    cnx.close()
    if row is not None :
        session['email'] = request.form['email']
        session['id'] = row[0]
        return redirect(url_for("list_transactions"))
    return redirect(url_for("get_login"))

