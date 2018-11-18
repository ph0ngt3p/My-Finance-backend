FROM python:3.6.7-alpine

WORKDIR /opt/app

RUN mkdir -p /opt/app && cd /opt/app

# Install packages
COPY requirements.txt .
RUN apk update \
    && apk upgrade \
    && apk add --no-cache --virtual .build-deps \
        linux-headers \
        gcc \
        musl-dev \
        python3-dev \
        libffi-dev \
    && apk add --no-cache openssl-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

COPY uwsgi.ini /etc/uwsgi/

# Copy the code
COPY . .

EXPOSE 5000
