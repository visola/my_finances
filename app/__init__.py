from datetime import date
from datetime import datetime
import decimal
from functools import wraps
import hashlib
import re
import uuid

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
import mysql.connector

from .config import *


app = Flask(__name__)

app.secret_key = MSQL_SECRET_KEY

def login_required(function_to_wrap):
    @wraps(function_to_wrap)
    def decorated_function(*args, **kwargs):
        if 'email' in session:
            return function_to_wrap(*args, **kwargs)
        return redirect(url_for("get_login"))
    return decorated_function

@app.route('/transactions')
@login_required
def list_transactions():
    cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                  host=MYSQL_HOST,
                                  database=MYSQL_DATABASE)
    cursor = cnx.cursor()
    select_transactions = ('''
        select t.id,t.description,c.category,t.date,t.value,a.name
        from transactions t
        left join categories c on t.category_id = c.id
        join accounts a on t.source_accnt_id = a.id
        where t.user_id=%s
        order by date desc
    ''')
    session_id_data = (session["id"],)
    cursor.execute(select_transactions, session_id_data)
    all_transactions = []
    for row in cursor:
        all_transactions.append({
            "id": row[0],
            "description": row[1],
            "category": row[2],
            "date": row[3],
            "value": row[4],
            "source_account":row[5]
        })
    cnx.close()
    return render_template("transactions/index.html", transactions=all_transactions)

@app.route('/transactions/new')
@login_required
def new_transaction():
    cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                  host=MYSQL_HOST,
                                  database=MYSQL_DATABASE)
    cursor = cnx.cursor()
    select_categories = ("select id,category from categories where user_id=%s")
    category_data = (session["id"],)
    cursor.execute(select_categories, category_data)
    all_categories = cursor.fetchall()
    select_accounts = ("select id,name from accounts where user_id=%s")
    account_data = (session["id"],)
    cursor.execute(select_accounts, account_data)
    all_accounts = cursor.fetchall()
    cnx.close()
    return render_template(
        "transactions/edit.html",
        categories=all_categories,
        date=datetime.now(),
        destination_accnt_id=None,
        accounts=all_accounts
    )

@app.route('/transactions/<transaction_id>')
@login_required
def edit_transaction(transaction_id):
    cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                  host=MYSQL_HOST,
                                  database=MYSQL_DATABASE)
    cursor = cnx.cursor()
    select_categories = ("select id,category from categories where user_id=%s")
    category_data = (session["id"],)
    cursor.execute(select_categories, category_data)
    all_categories = cursor.fetchall()
    select_accounts = ("select id,name from accounts where user_id=%s")
    account_data = (session["id"],)
    cursor.execute(select_accounts, account_data)
    all_accounts = cursor.fetchall()
    select_transaction = ('''
        select id,description,category_id,date,value,source_accnt_id,link_id
        from transactions
        where id=%s and user_id=%s
    ''')
    transaction_data = (int(transaction_id), session["id"])
    cursor.execute(select_transaction, transaction_data)
    row = cursor.fetchone()
    linked_transaction_accnt = None
    if row[6] is not None:
        linked_account = ("select source_accnt_id from transactions where link_id =%s and id<> %s")
        link_id_data = (row[6], int(transaction_id))
        cursor.execute(linked_account, link_id_data)
        linked_transaction_accnt = cursor.fetchone()[0]
    cnx.close()
    if row is None:
        return "Page not found."
    return render_template(
        "transactions/edit.html",
        accounts=all_accounts,
        categories=all_categories,
        category_id=row[2],
        date=row[3],
        description=row[1],
        destination_accnt_id=linked_transaction_accnt,
        id=row[0],
        source_accnt_id=row[5],
        value=row[4],
        link_id=row[6]
    )

@app.route('/transactions/save', methods=["POST"])
@login_required
def save_transactions():
    cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                  host=MYSQL_HOST,
                                  database=MYSQL_DATABASE)
    cursor = cnx.cursor()

    passed_id = request.form["id"]

    value = request.form["value"]
    if value == "":
        return "Value can not be empty."
    if session['preference'] == "pt-br":
        value = value.replace(",", ".")
    else:
        value = value.replace(",", "")
    reverse_value = float(value)*-1.0

    transaction_date = request.form["date"]
    if session['preference'] == "pt-br":
        transaction_date = datetime.strptime(request.form["date"], '%d/%m/%Y')
    elif session['preference'] == "en-us":
        transaction_date = datetime.strptime(request.form["date"], '%m/%d/%Y')
    else:
        return f"'{transaction_date}' Is not according to format."
    category_id = request.form['category_id']
    if category_id == "-1":
        category_id = None

    validate_source_accnt = ("select id from accounts where id = %s and user_id = %s")
    source_accnt_data = (request.form["source_accnt_id"], session["id"])
    cursor.execute(validate_source_accnt, source_accnt_data)
    cursor.fetchone()
    if cursor.rowcount == 0:
        cnx.close()
        return "Sorry, there was an error. 1"
    if request.form["destination_accnt_id"] != "-1":
        validate_destination_accnt = ("select id from accounts where id = %s and user_id = %s")
        destination_accnt_data = (request.form["destination_accnt_id"], session["id"])
        cursor.execute(validate_destination_accnt, destination_accnt_data)
        cursor.fetchone()
        if cursor.rowcount == 0:
            cnx.close()
            return "Sorry, there was an error. 2"

    select_categories = ("select category from categories where user_id=%s and id=%s")
    categories_data = (session["id"], category_id)
    cursor.execute(select_categories, categories_data)
    cursor.fetchone()
    if cursor.rowcount == 0 and category_id is not None:
        cnx.close()
        return "Sorry, there was an error. 3"

    reverse_transaction_id = None
    link_id = None
    if passed_id != "":
        select_transaction = ('''
            SELECT t.id, t.link_id, r.id
            FROM transactions t
            LEFT OUTER JOIN transactions r
                ON r.link_id = t.link_id
                and t.link_id IS NOT NULL
                AND t.user_id = r.user_id
                and t.id<>r.id
            WHERE t.id = %s AND t.user_id = %s
        ''')
        transaction_data = (passed_id, session["id"])
        cursor.execute(select_transaction, transaction_data)
        row = cursor.fetchone()
        if cursor.rowcount == 0:
            cnx.close()
            return "Sorry, there was an error. 4"
        link_id = row[1]
        reverse_transaction_id = row[2]

    if request.form["destination_accnt_id"] != "-1" and link_id is None:
        link_id = str(uuid.uuid4())

    if passed_id != "":
        update_transaction = ('''
            update transactions
            set description=%s, category_id=%s, date=%s, value=%s, source_accnt_id=%s, link_id=%s
            where id=%s
                and user_id = %s
        ''')
        transaction_data = (
            request.form["description"],
            category_id,
            transaction_date,
            value,
            request.form["source_accnt_id"],
            link_id,
            request.form["id"],
            session["id"]
        )
        cursor.execute(update_transaction, transaction_data)
    else:
        insert_transaction = ('''
            insert into transactions
            (description, user_id, category_id, date, value, source_accnt_id, link_id)
            values (%s, %s, %s, %s, %s, %s, %s)
        ''')
        transaction_data = (
            request.form["description"],
            session["id"],
            category_id,
            transaction_date,
            value,
            request.form["source_accnt_id"],
            link_id
        )
        cursor.execute(insert_transaction, transaction_data)

    if link_id is None:
        if reverse_transaction_id is not None:
            delete_linked_transactions = ("delete from transactions where id= %s")
            delete_data = (reverse_transaction_id, )
            cursor.execute(delete_linked_transactions, delete_data)
    else:
        if reverse_transaction_id is not None:
            update_transaction = ('''
                update transactions
                set description=%s, category_id=%s, date=%s, value=%s, source_accnt_id=%s, link_id=%s
                where id=%s and user_id = %s
            ''')
            transaction_data = (
                request.form["description"],
                category_id,
                transaction_date,
                reverse_value,
                request.form["destination_accnt_id"],
                link_id,
                reverse_transaction_id,
                session["id"]
            )
            cursor.execute(update_transaction, transaction_data)
        else:
            insert_transaction = ('''
                insert into transactions
                (description,user_id,category_id,date,value,source_accnt_id,link_id)
                values(%s,%s,%s,%s,%s,%s,%s)
            ''')
            transaction_data_insert = (
                request.form["description"],
                session["id"],
                category_id,
                transaction_date,
                reverse_value,
                request.form["destination_accnt_id"],
                link_id
            )
            cursor.execute(insert_transaction, transaction_data_insert)

    cnx.commit()
    cnx.close()
    return redirect(url_for("list_transactions"))

@app.route('/users/new')
def create_user():
    return render_template("users/edit.html")

@app.route('/users/save', methods=["POST"])
def save_users():
    cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                  host=MYSQL_HOST,
                                  database=MYSQL_DATABASE)
    cursor = cnx.cursor()
    select_users = ("select count(1) from users where email=%s")
    email_data = (request.form["email"],)
    cursor.execute(select_users, email_data)
    row = cursor.fetchone()
    if row[0] > 0:
        cnx.close()
        return redirect(url_for("create_user"))
    insert_user = ("insert into users(name,email,password) values(%s,%s,%s)")
    password = hashlib.sha256(request.form["password"].encode("utf-8")).hexdigest()
    user_data = (request.form["name"], request.form["email"], password)
    cursor.execute(insert_user, user_data)
    cnx.commit()
    cnx.close()
    return redirect(url_for("list_transactions"))

@app.route('/login', methods=["GET"])
def get_login():
    return render_template("login/index.html")

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('id', None)
    return redirect(url_for('get_login'))

@app.route('/login', methods=["POST"])
def login():
    cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                  host=MYSQL_HOST,
                                  database=MYSQL_DATABASE)
    cursor = cnx.cursor()
    select_users = ('''
        select u.id,u.name,p.preference
        from users u
        left outer join preferences p on p.user_id = u.id
        where email=%s and password=%s
    ''')
    password = hashlib.sha256(request.form["password"].encode("utf-8")).hexdigest()
    email_data = (request.form["email"], password)
    cursor.execute(select_users, email_data)
    row = cursor.fetchone()
    cnx.close()
    if row is not None:
        session['email'] = request.form['email']
        session['id'] = row[0]
        session['name'] = row[1]
        if row[2] is None:
            session['preference'] = "en-us"
        else:
            session['preference'] = row[2]
        return redirect(url_for("dashboard"))
    return redirect(url_for("get_login"))

@app.route('/categories')
@login_required
def list_categories():
    cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                  host=MYSQL_HOST,
                                  database=MYSQL_DATABASE)
    cursor = cnx.cursor()
    select_categories = ("select * from categories where user_id=%s")
    session_id_data = (session["id"],)
    cursor.execute(select_categories, session_id_data)
    all_categories = []
    for row in cursor:
        all_categories.append({"id": row[0], "description": row[1]})
    cnx.close()
    return render_template("categories/index.html", categories=all_categories)

@app.route('/categories/new')
@login_required
def new_category():
    return render_template("categories/edit.html")

@app.route('/categories/<category_id>')
@login_required
def edit_category(category_id):
    cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                  host=MYSQL_HOST,
                                  database=MYSQL_DATABASE)
    cursor = cnx.cursor()
    select_category = ("select * from categories where id=%s and user_id=%s")
    category_data = (int(category_id), session["id"])
    cursor.execute(select_category, category_data)
    row = cursor.fetchone()
    cnx.close()
    if row is None:
        return "Page not found."
    return render_template("categories/edit.html", id=row[0], category=row[1])

@app.route('/categories/save', methods=["POST"])
@login_required
def save_categories():
    cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                  host=MYSQL_HOST,
                                  database=MYSQL_DATABASE)
    cursor = cnx.cursor()
    if request.form["id"] != "":
        update_category = ("update categories set category=%s where id=%s and user_id = %s")
        category_data = (request.form["category"], request.form["id"], session["id"])
        cursor.execute(update_category, category_data)
    else:
        insert_category = ("insert into categories(category,user_id) values(%s,%s)")
        category_data = (request.form["category"], session["id"])
        cursor.execute(insert_category, category_data)
    cnx.commit()
    cnx.close()
    return redirect(url_for("list_categories"))

@app.route('/dashboard')
@login_required
def dashboard():
    cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                  host=MYSQL_HOST,
                                  database=MYSQL_DATABASE)
    cursor = cnx.cursor()
    count_c = ('''
        select count(t.id),c.category
        from transactions t
        join categories c
        where t.date between %s and %s
            and t.category_id=c.id
            and t.user_id =%s
        group by t.category_id
        order by c.category asc
    ''')
    end_date_c = date.today()
    start_date_c = date.fromordinal(end_date_c.toordinal()-30)
    select_count_c = (start_date_c, end_date_c, session["id"])
    cursor.execute(count_c, select_count_c)
    counts = {}
    for row in cursor:
        counts[row[1]] = row[0]
    count_c = ('''
            select count(t.id),c.category
            from transactions t
            join categories c
            where t.date between %s and %s
            and t.category_id=c.id
            and t.user_id =%s
            and link_id is not null
            group by t.category_id
            order by c.category asc
        ''')
    end_date_c = date.today()
    start_date_c = date.fromordinal(end_date_c.toordinal()-30)
    select_count_c = (start_date_c, end_date_c, session["id"])
    cursor.execute(count_c, select_count_c)
    for row in cursor:
        counts[row[1]] = counts[row[1]] - int(row[0]/2)
    count_a = ('''
        select count(t.id),a.name
        from transactions t
        join accounts a
        where t.date between %s and %s
            and t.source_accnt_id=a.id
            and t.user_id = %s
        group by t.source_accnt_id
        order by name asc
    ''')
    end_date_a = date.today()
    start_date_a = date.fromordinal(end_date_c.toordinal()-30)
    select_count_a = (start_date_a, end_date_a, session["id"])
    cursor.execute(count_a, select_count_a)
    all_accounts = []
    for row in cursor:
        all_accounts.append({"count": row[0], "account": row[1]})
    cnx.close()
    return render_template(
        "home_page/index.html",
        count_categories=counts,
        count_accounts=all_accounts
    )

@app.route('/accounts')
@login_required
def list_accounts():
    cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                  host=MYSQL_HOST,
                                  database=MYSQL_DATABASE)
    cursor = cnx.cursor()
    select_accounts = ("select id,name,user_id,type from accounts where user_id=%s")
    session_id_data = (session["id"],)
    cursor.execute(select_accounts, session_id_data)
    all_accounts = []
    for row in cursor:
        all_accounts.append({"id": row[0], "name": row[1], "user_id": row[2], "type": row[3]})
    cnx.close()
    return render_template("accounts/index.html", accounts=all_accounts)

@app.route('/accounts/new')
@login_required
def new_account():
    return render_template("accounts/edit.html")

@app.route('/accounts/<account_id>')
@login_required
def edit_accounts(account_id):
    cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                  host=MYSQL_HOST,
                                  database=MYSQL_DATABASE)
    cursor = cnx.cursor()
    select_accounts = ("select id,name,user_id,type from accounts where id=%s and user_id=%s")
    account_data = (int(account_id), session["id"])
    cursor.execute(select_accounts, account_data)
    row = cursor.fetchone()
    cnx.close()
    if row is None:
        return "Page not found."
    return render_template(
        "accounts/edit.html",
        id=row[0],
        name=row[1],
        user_id=row[2],
        type=row[3]
    )

@app.route('/accounts/save', methods=["POST"])
@login_required
def save_accounts():
    cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                  host=MYSQL_HOST,
                                  database=MYSQL_DATABASE)
    cursor = cnx.cursor()
    if request.form["id"] != "":
        update_accounts = ("update accounts set name=%s,type=%s where id=%s and user_id = %s")
        account_data = (
            request.form["name"],
            request.form["type"],
            request.form["id"],
            session["id"]
        )
        cursor.execute(update_accounts, account_data)
    else:
        insert_accounts = ("insert into accounts(name,user_id,type) values(%s,%s,%s)")
        account_data = (request.form["name"], session["id"], request.form["type"])
        cursor.execute(insert_accounts, account_data)
    cnx.commit()
    cnx.close()
    return redirect(url_for("list_accounts"))

@app.route('/profile')
@login_required
def profile_page():
    cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                  host=MYSQL_HOST,
                                  database=MYSQL_DATABASE)
    cursor = cnx.cursor()
    select_preference = ("select preference from preferences where user_id=%s")
    preference_data = (session["id"],)
    cursor.execute(select_preference, preference_data)
    row = cursor.fetchone()
    cnx.close()
    if row is None:
        return render_template("profile/index.html", preference=session['preference'])
    return render_template("profile/index.html", preference=row[0])

@app.route('/preference/new')
@login_required
def new_preference():
    return render_template("profile/preferences/edit.html")

@app.route('/profile/prefences')
@login_required
def user_prefences():
    cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                  host=MYSQL_HOST,
                                  database=MYSQL_DATABASE)
    cursor = cnx.cursor()
    select_preference = ("select preference from preferences where user_id=%s")
    preference_data = (session["id"],)
    cursor.execute(select_preference, preference_data)
    row = cursor.fetchone()
    cnx.close()
    if row is None:
        return render_template("profile/preferences.edit.html", preference=session['preference'])
    return render_template("profile/preferences.edit.html", preference=row[0])

@app.route('/preferences/save', methods=["POST"])
@login_required
def save_preferences():
    cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                  host=MYSQL_HOST,
                                  database=MYSQL_DATABASE)
    cursor = cnx.cursor()
    if request.form["exists"] == "True":
        update_preferences = ("update preferences set preference=%s where user_id = %s")
        preference_data = (request.form["preference"], session["id"])
        cursor.execute(update_preferences, preference_data)
    else:
        insert_preferences = ("insert into preferences(user_id,preference) values(%s,%s)")
        preference_data = (session["id"], request.form["preference"])
        cursor.execute(insert_preferences, preference_data)
    cnx.commit()
    cnx.close()
    session['preference'] = request.form["preference"]
    return redirect(url_for("profile_page"))


@app.context_processor
def formatters():
    def format_currency(value):
        preference = session['preference']
        if preference == "pt-br":
            return "R$ " + str(value).replace(".", ",")
        return "$ {0:.2f}".format(value)

    def format_number(value):
        if not isinstance(value, decimal.Decimal):
            value = 0.0
        preference = session['preference']
        if preference == "pt-br":
            return  str(value).replace(".", ",")
        return "{0:.2f}".format(value)

    def format_date(to_format):
        preference = session['preference']
        if preference == "pt-br":
            return datetime.strftime(to_format, '%d/%m/%Y')
        return datetime.strftime(to_format, '%m/%d/%Y')

    return dict(
        format_currency=format_currency,
        format_number=format_number,
        format_date=format_date
    )
