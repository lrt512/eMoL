# Build stage
# Temporary so we can build non-wheel packages in the venv
# This prevents needing buld-essential in the deployed container.
FROM python:3.12-slim as builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev

# Set up virtual environment
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install Python dependencies
COPY requirements/prod.txt /tmp/requirements.txt
RUN pip install --upgrade pip && \
    pip install wheel && \
    pip install -r /tmp/requirements.txt

# /Build stage

# Application stage
# This is the container we will deploy in Lightsail
FROM python:3.12-slim
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql postgresql-client \
    nginx certbot python3-certbot-nginx \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up application directory
WORKDIR /app
COPY emol/ /app/

# Configure Nginx
RUN rm /etc/nginx/sites-enabled/default
COPY docker_files/nginx.conf /etc/nginx/sites-enabled/

# Expose port for Nginx
EXPOSE 80

# Copy and set entrypoint script
COPY docker_files/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# /Application stage