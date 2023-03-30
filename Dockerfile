FROM ubuntu:22.04

WORKDIR /app
COPY emol/ /app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y nginx \
    mysql-server libmysqlclient-dev redis-server \
    build-essential python3 python3-dev python3-venv python3-pip

COPY requirements/ /tmp/requirements/

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN /venv/bin/pip install --upgrade pip
RUN /venv/bin/pip install wheel
RUN /venv/bin/pip install -r /tmp/requirements/dev.txt

RUN rm /etc/nginx/sites-enabled/default
COPY docker_files/nginx.conf /etc/nginx/sites-enabled/

EXPOSE 80

CMD service nginx start && gunicorn --bind 0.0.0.0:8000 myproject.wsgi
