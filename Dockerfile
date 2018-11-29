###########
# BUILDER #
###########

# Base Image
FROM python:3.6.7-alpine as builder

# Install Requirements
COPY requirements.txt /
RUN apk update \
    && apk upgrade \
    && apk add --no-cache \
        linux-headers \
        gcc \
        musl-dev \
        python3-dev \
        libffi-dev \
        openssl-dev

RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt


#########
# FINAL #
#########
FROM python:3.6.7-alpine

WORKDIR /opt/app

RUN mkdir -p /opt/app && cd /opt/app

# Install Requirements
COPY --from=builder /wheels /wheels
RUN apk add --no-cache libcrypto1.0 libssl1.0 && \
    pip install --no-cache /wheels/* && \
    rm -rf /wheels

COPY uwsgi.ini /etc/uwsgi/
COPY docker-entrypoint.sh /usr/local/bin/
RUN ln -s usr/local/bin/docker-entrypoint.sh / # backwards compat
ENTRYPOINT ['docker-entrypoint.sh']

# Copy the code
COPY . .

CMD ['uwsgi', '--ini', '/etc/uwsgi/uwsgi.ini']

EXPOSE 5000
