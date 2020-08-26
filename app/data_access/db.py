from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import (MYSQL_PASSWORD, MYSQL_USER, MYSQL_HOST, MYSQL_DATABASE,)

connection = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"
engine = create_engine(connection)
Session = sessionmaker(bind=engine)

def create_session():
    return Session()
