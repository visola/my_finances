FROM ubuntu:latest

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y && \
    apt-get install -y curl gnupg2 python3 python3-venv python3-setuptools tzdata unzip xvfb wget

# Install Chrome
RUN curl https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /chrome.deb
RUN dpkg -i /chrome.deb || apt-get install -yf

# Set up Chromedriver Environment variables
ENV CHROMEDRIVER_VERSION LATEST_RELEASE_88.0.4324
ENV CHROMEDRIVER_DIR /chromedriver
RUN mkdir $CHROMEDRIVER_DIR

RUN wget -q --continue -P $CHROMEDRIVER_DIR "https://chromedriver.storage.googleapis.com/88.0.4324.96/chromedriver_linux64.zip"
RUN unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR

ENV PATH $CHROMEDRIVER_DIR:$PATH

COPY ./app /opt/app
COPY ./alembic /opt/alembic
COPY ./alembic.ini /opt/alembic.ini
COPY ./setup.py /opt/setup.py
COPY ./integration_tests /opt/integration_tests

WORKDIR /opt
RUN python3 setup.py install

CMD [ "/bin/bash", "-c", "integration_tests/run_tests.sh" ]
