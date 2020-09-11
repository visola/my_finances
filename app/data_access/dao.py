import hashlib
from sqlalchemy import desc
from app.data_access.schema import User, Category, Account, Preference, Transaction

class UserDAO():
    def __init__(self, session):
        self.session = session

    def create(self, *, email, name, password):
        user = User(
            email=email,
            name=name,
            password=hashlib.sha256(password.encode("utf-8")).hexdigest(),
        )
        self.session.add(user)
        return user


    def find_by_email(self, email):
        return self.session.query(User) \
        .filter_by(email=email) \
        .first()

    def find_by_email_and_password(self, email, password):
        return self.session.query(User) \
        .filter_by(
            email=email,
            password=hashlib.sha256(password.encode("utf-8")).hexdigest(),
        ).first()



class CategoryDAO():
    def __init__(self, session):
        self.session = session

    def find_by_user_id(self, user_id):
        return self.session.query(Category) \
          .filter_by(user_id=user_id) \
          .all()

    def find_by_id_and_user_id(self, category_id, user_id):
        return self.session.query(Category) \
          .filter_by(
              id=category_id,
              user_id=user_id
          ).first()

    def save(self, *, category_id=None, name, user_id):
        if category_id is None:
            category = Category(user_id=user_id)
            self.session.add(category)
        else:
            category = self.find_by_id_and_user_id(category_id, user_id)

        category.name = name

        return category

class AccountDAO():
    def __init__(self, session):
        self.session = session

    def find_by_user_id(self, user_id):
        return self.session.query(Account) \
          .filter_by(user_id=user_id) \
          .all()

    def find_by_id_and_user_id(self, account_id, user_id):
        return self.session.query(Account) \
          .filter_by(
              id=account_id,
              user_id=user_id
          ).first()

    def save(self, *, account_id=None, name, user_id, account_type):
        if account_id is None:
            account = Account(user_id=user_id)
            self.session.add(account)
        else:
            account = self.find_by_id_and_user_id(account_id, user_id)

        account.name = name
        account.type = account_type

        return account

class PreferenceDAO():
    def __init__(self, session):
        self.session = session

    def find_by_user_id(self, *, user_id):
        return self.session.query(Preference) \
          .filter_by(user_id=user_id) \
          .first()

    def save(self, *, user_id, preference):
        loaded_preference = self.find_by_user_id(user_id=user_id)
        if loaded_preference is None:
            loaded_preference = Preference(user_id=user_id)
            self.session.add(loaded_preference)

        loaded_preference.preference = preference
        return loaded_preference

class TransactionDAO():
    def __init__(self, session):
        self.session = session

    def find_by_user_id(self, *, user_id):
        return self.session.query(Transaction) \
          .filter_by(user_id=user_id) \
          .order_by(desc(Transaction.date)) \
          .all()

    def find_by_id_and_user_id(self, *, transaction_id, user_id):
        return self.session.query(Transaction) \
            .filter_by(
                id=transaction_id,
                user_id=user_id
            ).first()

    def find_linked_transaction(self, *, link_id, user_id, transaction_id):
        return self.session.query(Transaction) \
            .filter_by(
                link_id=link_id,
                user_id=user_id,
            ).filter(
                Transaction.id != transaction_id
            ).first()

    def delete_by_id(self, *, transaction_id, user_id):
        return self.session.query(Transaction) \
            .filter_by(
                id=transaction_id,
                user_id=user_id
            ).delete()

    def save(self, *, transaction_id=None, description, user_id,
             category_id, date, value, source_accnt_id, link_id):
        if transaction_id is None:
            transaction = Transaction(user_id=user_id)
            self.session.add(transaction)
        else:
            transaction = self.find_by_id_and_user_id(
                transaction_id=transaction_id,
                user_id=user_id
            )

        transaction.description = description
        transaction.category_id = category_id
        transaction.date = date
        transaction.value = value
        transaction.source_accnt_id = source_accnt_id
        transaction.link_id = link_id

        return transaction
