from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import *

engine = create_engine(f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}")
Session = sessionmaker(bind=engine)

def create_session():
  return Session()
