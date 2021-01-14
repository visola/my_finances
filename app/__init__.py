from datetime import date
from datetime import datetime
import decimal
from functools import wraps
import re
import uuid
from os import path

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
import mysql.connector
from prometheus_flask_exporter import PrometheusMetrics

from app.data_access.dao import UserDAO, CategoryDAO, AccountDAO, PreferenceDAO, TransactionDAO
from app.data_access.db import create_session
from app import locale_format

from .config_loader import *

app = Flask(__name__)
app.secret_key = APP_SECRET_KEY

metrics = PrometheusMetrics(app, defaults_prefix="myfinances")

def login_required(function_to_wrap):
    @wraps(function_to_wrap)
    def decorated_function(*args, **kwargs):
        if 'email' in session:
            return function_to_wrap(*args, **kwargs)
        return redirect(url_for("get_login"))
    return decorated_function

def parse_currency(value):
    if value == "":
        return False, None

    if session['preference'] == "pt-br":
        return True, float(value.replace(",", "."))

    return True, float(value.replace(",", ""))

def parse_date(date_string):
    if session['preference'] == "pt-br":
        return True, datetime.strptime(date_string, '%d/%m/%Y')

    return True, datetime.strptime(date_string, '%m/%d/%Y')

def validate_accounts(db_session, *account_ids, user_id):
    account_dao = AccountDAO(db_session)
    for account_id in account_ids:
        if account_id is None or int(account_id) == -1:
            continue

        print(f"Validating account '{account_id}'")
        account = account_dao.find_by_id_and_user_id(
            account_id=account_id,
            user_id=user_id
        )
        if account is None:
            return False
    return True

def validate_categories(db_session, *category_ids, user_id):
    category_dao = CategoryDAO(db_session)
    for category_id in category_ids:
        if category_id is None or int(category_id) == -1:
            continue

        category = category_dao.find_by_id_and_user_id(
            category_id=category_id,
            user_id=user_id
        )
        if category is None:
            return False
    return True

@app.route('/transactions')
@login_required
def list_transactions():
    db_session = create_session()
    transaction_dao = TransactionDAO(db_session)
    all_transactions = transaction_dao.find_by_user_id(user_id=session["id"])
    category_dao = CategoryDAO(db_session)
    categories = category_dao.find_by_user_id(session["id"])
    account_dao = AccountDAO(db_session)
    accounts = account_dao.find_by_user_id(session["id"])
    db_session.close()
    return render_template("transactions/index.html",
                           transactions=all_transactions,
                           categories=categories,
                           accounts=accounts)

@app.route('/transactions/new')
@login_required
def new_transaction():
    db_session = create_session()
    category_dao = CategoryDAO(db_session)
    categories = category_dao.find_by_user_id(session["id"])
    account_dao = AccountDAO(db_session)
    accounts = account_dao.find_by_user_id(session["id"])
    db_session.close()
    return render_template(
        "transactions/edit.html",
        categories=categories,
        date=datetime.now(),
        destination_accnt_id=None,
        accounts=accounts
    )

@app.route('/transactions/<transaction_id>')
@login_required
def edit_transaction(transaction_id):
    db_session = create_session()
    category_dao = CategoryDAO(db_session)
    categories = category_dao.find_by_user_id(session["id"])
    account_dao = AccountDAO(db_session)
    accounts = account_dao.find_by_user_id(session["id"])
    transaction_dao = TransactionDAO(db_session)
    transaction = transaction_dao.find_by_id_and_user_id(
        transaction_id=transaction_id,
        user_id=session["id"]
    )
    destination_accnt_id = None
    linked_transaction_id = None
    if transaction.link_id is not None:
        linked_transaction = transaction_dao.find_linked_transaction(
            link_id=transaction.link_id,
            user_id=session["id"],
            transaction_id=transaction.id
        )
        destination_accnt_id = linked_transaction.source_accnt_id
        linked_transaction_id = linked_transaction.id
    db_session.close()
    return render_template(
        "transactions/edit.html",
        categories=categories,
        accounts=accounts,
        category_id=transaction.category_id,
        date=transaction.date,
        description=transaction.description,
        destination_accnt_id=destination_accnt_id,
        id=transaction.id,
        source_accnt_id=transaction.source_accnt_id,
        value=transaction.value,
        link_id=linked_transaction_id
    )

@app.route('/transactions/save', methods=["POST"])
@login_required
def post_transactions():

    valid, value = parse_currency(request.form["value"])
    if not valid:
        return "Value can not be empty."

    if value < 0:
        value = value*-1

    if request.form["direction"] == "1":
        value = value*-1

    valid, transaction_date = parse_date(request.form["date"])
    if not valid:
        return f"'{request.form['date']}' Is not according to format."

    db_session = create_session()

    if validate_accounts(
            db_session,
            request.form["source_accnt_id"],
            request.form["destination_accnt_id"],
            user_id=session["id"]) is False:
        db_session.close()
        return "Sorry, there was an error. Invalid account ID."

    if validate_categories(
            db_session,
            request.form["category_id"],
            user_id=session["id"]) is False:
        db_session.close()
        return "Sorry, there was an error. Invalid category ID."

    transaction_dao = TransactionDAO(db_session)

    reverse_transaction = None
    link_id = None
    transaction_id = request.form["id"] or None
    if transaction_id is not None:
        transaction = transaction_dao.find_by_id_and_user_id(
            transaction_id=request.form["id"],
            user_id=session["id"]
        )
        if transaction is None:
            db_session.close()
            return "Sorry, there was an error. Invalid transaction ID."
        if transaction.link_id is not None:
            link_id = transaction.link_id
            reverse_transaction = transaction_dao.find_linked_transaction(
                link_id=link_id,
                user_id=session["id"],
                transaction_id=transaction.id
            )

    if request.form["destination_accnt_id"] != "-1":
        link_id = str(uuid.uuid4())
        reverse_transaction_id = None
        if reverse_transaction is not None:
            reverse_transaction_id = reverse_transaction.id
        transaction_dao.save(
            transaction_id=reverse_transaction_id,
            description=request.form["description"],
            user_id=session["id"],
            category_id=request.form["category_id"],
            date=transaction_date,
            value=value*-1,
            source_accnt_id=request.form["destination_accnt_id"],
            link_id=link_id
        )

    if reverse_transaction is not None and request.form["destination_accnt_id"] == "-1":
        transaction_dao.delete_by_id(
            transaction_id=reverse_transaction.id,
            user_id=session["id"]
        )
        link_id = None

    transaction_dao.save(
        transaction_id=transaction_id,
        description=request.form["description"],
        user_id=session["id"],
        category_id=request.form["category_id"],
        date=transaction_date,
        value=value,
        source_accnt_id=request.form["source_accnt_id"],
        link_id=link_id
    )


    db_session.commit()
    db_session.close()
    return redirect(url_for("list_transactions"))

@app.route('/users/new')
def create_user():
    return render_template("users/edit.html")

@app.route('/users/save', methods=["POST"])
def save_users():
    db_session = create_session()
    user_dao = UserDAO(db_session)
    preferences_dao = PreferenceDAO(db_session)

    maybe_user = user_dao.find_by_email(request.form["email"])
    if maybe_user is not None:
        return redirect(url_for("create_user"))

    user = user_dao.create(
        email=request.form["email"],
        name=request.form["name"],
        password=request.form["password"],
    )

    db_session.commit()

    preferences_dao.save(
        user_id=user.id,
        preference="en-us",
    )

    db_session.commit()
    db_session.close()
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
    db_session = create_session()
    maybe_user = UserDAO(db_session) \
        .find_by_email_and_password(request.form["email"], request.form["password"])

    if maybe_user is None:
        db_session.close()
        return redirect(url_for("get_login"))

    preferences_dao = PreferenceDAO(db_session)
    preference = preferences_dao.find_by_user_id(user_id=maybe_user.id)

    session['preference'] = preference.preference
    session['email'] = maybe_user.email
    session['id'] = maybe_user.id
    session['name'] = maybe_user.name
    db_session.close()
    return redirect(url_for("dashboard"))

@app.route('/categories')
@login_required
def list_categories():
    db_session = create_session()
    categories_dao = CategoryDAO(db_session)

    categories = categories_dao.find_by_user_id(session["id"])
    db_session.close()
    return render_template("categories/index.html", categories=categories)

@app.route('/categories/new')
@login_required
def new_category():
    return render_template("categories/edit.html", category={})

@app.route('/categories/<category_id>')
@login_required
def edit_category(category_id):
    db_session = create_session()
    categories_dao = CategoryDAO(db_session)

    category = categories_dao.find_by_id_and_user_id(category_id, session["id"])
    db_session.close()
    return render_template("categories/edit.html", category=category)

@app.route('/categories/save', methods=["POST"])
@login_required
def save_category():
    db_session = create_session()
    categories_dao = CategoryDAO(db_session)

    category_id = request.form["id"]
    if category_id == "":
        category_id = None

    categories_dao.save(
        category_id=category_id,
        name=request.form["name"],
        user_id=session["id"],
    )

    db_session.commit()
    db_session.close()
    return redirect(url_for("list_categories"))

@app.route('/dashboard')
@login_required
def dashboard():
    cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                  host=MYSQL_HOST,
                                  database=MYSQL_DATABASE)
    cursor = cnx.cursor()
    count_c = ('''
        select count(t.id),c.name
        from transactions t
        join categories c
        where t.date between %s and %s
            and t.category_id=c.id
            and t.user_id =%s
        group by t.category_id
        order by c.name asc
    ''')
    end_date_c = date.today()
    start_date_c = date.fromordinal(end_date_c.toordinal()-30)
    select_count_c = (start_date_c, end_date_c, session["id"])
    cursor.execute(count_c, select_count_c)
    counts = {}
    for row in cursor:
        counts[row[1]] = row[0]
    count_c = ('''
            select count(t.id),c.name
            from transactions t
            join categories c
            where t.date between %s and %s
            and t.category_id=c.id
            and t.user_id =%s
            and link_id is not null
            group by t.category_id
            order by c.name asc
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
    db_session = create_session()
    accounts_dao = AccountDAO(db_session)

    accounts = accounts_dao.find_by_user_id(session["id"])
    db_session.close()
    return render_template("accounts/index.html", accounts=accounts)

@app.route('/accounts/new')
@login_required
def new_account():
    return render_template("accounts/edit.html", account={})

@app.route('/accounts/<account_id>')
@login_required
def edit_accounts(account_id):
    db_session = create_session()
    accounts_dao = AccountDAO(db_session)

    account = accounts_dao.find_by_id_and_user_id(account_id, session["id"])
    db_session.close()
    return render_template("accounts/edit.html", account=account)

@app.route('/accounts/save', methods=["POST"])
@login_required
def save_accounts():
    db_session = create_session()
    accounts_dao = AccountDAO(db_session)

    account_id = request.form["id"]
    if account_id == "":
        account_id = None

    accounts_dao.save(
        account_id=account_id,
        name=request.form["name"],
        user_id=session["id"],
        account_type=request.form["type"],
    )

    db_session.commit()
    db_session.close()
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


@app.route('/profile/prefences')
@login_required
def user_prefences():
    db_session = create_session()
    preferences_dao = PreferenceDAO(db_session)

    preferences = preferences_dao.find_by_user_id(user_id=session["id"])
    db_session.close()
    return render_template("profile/preferences.edit.html", preferences=preferences)


@app.route('/preferences/save', methods=["POST"])
@login_required
def save_preferences():
    db_session = create_session()
    preferences_dao = PreferenceDAO(db_session)

    preferences_dao.save(
        user_id=session["id"],
        preference=request.form["preference"],
    )

    db_session.commit()
    db_session.close()
    session['preference'] = request.form["preference"]
    return redirect(url_for("profile_page"))


@app.context_processor
def formatters():
    def wrap_format_currency(value):
        return locale_format.format_currency(value, session["preference"])

    def wrap_format_number(value):
        return locale_format.format_number(value, session["preference"])

    def wrap_format_date(to_format):
        return locale_format.format_date(to_format, session["preference"])

    return dict(
        format_currency=wrap_format_currency,
        format_number=wrap_format_number,
        format_date=wrap_format_date
    )
