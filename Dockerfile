FROM ubuntu:latest

RUN apt-get update -y && \
    apt-get install -y python3 python3-venv python3-setuptools

COPY ./app /opt/app
COPY ./alembic /opt/alembic
COPY ./alembic.ini /opt/alembic.ini
COPY ./setup.py /opt/setup.py

WORKDIR /opt
RUN python3 setup.py install

CMD [ "gunicorn", "-b", "0.0.0.0:5000", "app:app" ]
