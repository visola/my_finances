import os

from .config import (MYSQL_PASSWORD, MYSQL_USER, MYSQL_HOST, MYSQL_DATABASE, MSQL_SECRET_KEY,)

if os.environ.get('MYSQL_DATABASE') is not None:
    MYSQL_DATABASE=os.environ.get('MYSQL_DATABASE')

if os.environ.get('MYSQL_HOST') is not None:
    MYSQL_HOST=os.environ.get('MYSQL_HOST')

if os.environ.get('MYSQL_PASSWORD') is not None:
    MYSQL_PASSWORD=os.environ.get('MYSQL_PASSWORD')

if os.environ.get('MYSQL_USER') is not None:
    MYSQL_USER=os.environ.get('MYSQL_USER')

if os.environ.get('MSQL_SECRET_KEY') is not None:
    MSQL_SECRET_KEY=os.environ.get('MSQL_SECRET_KEY')