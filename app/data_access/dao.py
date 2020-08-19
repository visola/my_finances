import hashlib

from app.data_access.schema import User, Category

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


class CategoryDAO():
  def __init__(self, session):
    self.session = session

  def save(self, *, id=None, name, user_id):
      self.session.add(Category(
        id=id,
        name=name,
        user_id=user_id
      ))

  def find_by_user_id(self,user_id):
    return self.session.query(Category) \
      .filter_by(user_id=user_id) \
      .all()

  def find_by_id_and_user_id(self,id,user_id):
    return self.session.query(Category) \
      .filter_by(
        id=id,
        user_id=user_id
      ).first()