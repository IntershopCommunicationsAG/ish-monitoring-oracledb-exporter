ARG PYTHON_VERSION=3.7

FROM python:${PYTHON_VERSION}-slim-buster

RUN apt-get update \
    && apt-get install -yqq libaio1 unzip wget \
    && mkdir -p /opt/oracle \
    && cd /opt/oracle \
    && wget https://s3.cn-north-1.amazonaws.com.cn/ext-etl-data/instantclient-basic-linux.x64-12.1.0.2.0.zip \
    && unzip instantclient-basic-linux.x64-12.1.0.2.0.zip \
    && cd /opt/oracle/instantclient_12_1 \
    && ln -s libclntsh.so.12.1 libclntsh.so \
    && ln -s libocci.so.12.1 libocci.so \
    && echo /opt/oracle/instantclient_12_1 > /etc/ld.so.conf.d/oracle-instantclient.conf \
    && ldconfig

ENV PYTHONDONTWRITEBYTECODE=True

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

COPY . /usr/src/app

CMD gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:8000 manage:app
