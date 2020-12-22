import configparser
import os

config = configparser.ConfigParser()

config.read('config.ini')

default = config['DEFAULT']

if 'APP_SECRET_KEY' in default:
    APP_SECRET_KEY=default['APP_SECRET_KEY']

if os.environ.get('APP_SECRET_KEY') is not None:
    APP_SECRET_KEY=os.environ.get('APP_SECRET_KEY')

if APP_SECRET_KEY is None:
    raise Exception('APP_SECRET_KEY not defined')

if 'MYSQL_DATABASE' in default:
    MYSQL_DATABASE=default['MYSQL_DATABASE']

if os.environ.get('MYSQL_DATABASE') is not None:
    MYSQL_DATABASE=os.environ.get('MYSQL_DATABASE')

if MYSQL_DATABASE is None:
    raise Exception('MYSQL_DATABASE not defined')

if 'MYSQL_HOST' in default:
    MYSQL_HOST=default['MYSQL_HOST']

if os.environ.get('MYSQL_HOST') is not None:
    MYSQL_HOST=os.environ.get('MYSQL_HOST')

if MYSQL_HOST is None:
    raise Exception('MYSQL_HOST not defined')

if 'MYSQL_PASSWORD' in default:
    MYSQL_PASSWORD=default['MYSQL_PASSWORD']

if os.environ.get('MYSQL_PASSWORD') is not None:
    MYSQL_PASSWORD=os.environ.get('MYSQL_PASSWORD')

if MYSQL_PASSWORD is None:
    raise Exception('MYSQL_PASSWORD not defined')

if 'MYSQL_USER' in default:
    MYSQL_USER=default['MYSQL_USER']

if os.environ.get('MYSQL_USER') is not None:
    MYSQL_USER=os.environ.get('MYSQL_USER')

if MYSQL_USER is None:
    raise Exception('MYSQL_USER not defined')
