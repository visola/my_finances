FROM ubuntu:latest

RUN apt-get update -y && \
    apt-get install -y python3 python3-venv python3-setuptools

COPY ./app /opt/app
COPY ./setup.py /opt/setup.py

WORKDIR /opt
RUN python3 setup.py install

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]
