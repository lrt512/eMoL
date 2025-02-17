FROM ubuntu:22.04

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    TZ=America/Toronto \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    awscli \
    nginx \
    certbot \
    python3-certbot-nginx \
    git \
    python3-venv \
    python3-pip \
    build-essential \
    pkg-config \
    python3-dev \
    libmysqlclient-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry - fixed installation and PATH
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry

# Create application directory
RUN mkdir -p /opt/emol/emol

# Copy setup files
COPY setup_files /opt/emol/setup_files
RUN chmod +x /opt/emol/setup_files/*.sh

# Configure AWS CLI for LocalStack
RUN mkdir -p ~/.aws && \
    echo "[default]\n\
aws_access_key_id = test\n\
aws_secret_access_key = test\n\
region = ca-central-1\n\
output = json" > ~/.aws/credentials && \
    echo "[default]\n\
region = ca-central-1\n\
output = json" > ~/.aws/config

# Copy application files
COPY . /opt/emol/
WORKDIR /opt/emol/emol

# Set up nginx
RUN rm -f /etc/nginx/sites-enabled/default && \
    cp /opt/emol/setup_files/configs/nginx.conf /etc/nginx/sites-enabled/

# Set up emol service
RUN cp /opt/emol/setup_files/configs/emol /etc/init.d/ && \
    chmod +x /etc/init.d/emol

# Install dependencies and set up environment
RUN cd /opt/emol && \
    poetry install --only main && \
    chown -R www-data:www-data /opt/emol

EXPOSE 80

# Start services
CMD service nginx start && \
    cd /opt/emol && \
    poetry run python manage.py migrate && \
    poetry run python manage.py collectstatic --noinput && \
    poetry run python manage.py createcachetable && \
    /etc/init.d/emol start && \
    tail -f /var/log/nginx/error.log
