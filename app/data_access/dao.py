import hashlib

from app.data_access.schema import User

class UserDAO():
  def __init__(self, session):
    self.session = session

  def create(self, *, email, name, password):
    self.session.add(User(
      email=email,
      name=name,
      password=hashlib.sha256(password.encode("utf-8")).hexdigest(),
    ))

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
