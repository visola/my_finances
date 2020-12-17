from os import path
from setuptools import setup

if not path.exists('config.ini'):
    with open('config.ini', 'w') as f:
      f.write('''
[DEFAULT]
APP_SECRET_KEY='{CRYPTO_KEY_FOR_SESSION}'
MYSQL_DATABASE='{DATABASE_NAME}'
MYSQL_HOST='{DATABASE_HOST}'
MYSQL_PASSWORD='{DATABASE_PASSWORD}'
MYSQL_USER='{DATABASE_USERNAME}'
      ''')

setup(
    name='my_finances',
    version='1.0',
    long_description=__doc__,
    packages=['app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
      'Flask==1.1.2',
      'gunicorn==20.0.4',
      'mysql-connector-python==8.0.20',
      'pylint>=2',
      'pytest==6.0.2',
      'pytest-cov==2.10.1',
      'sqlalchemy>=1.3,<1.4',
    ]
)
