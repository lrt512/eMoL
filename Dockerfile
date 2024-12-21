FROM ubuntu:22.04

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Toronto

COPY setup_files/bootstrap_system.sh /tmp
RUN chmod +x /tmp/bootstrap_system.sh
RUN /tmp/bootstrap_system.sh

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

EXPOSE 80
WORKDIR /opt/emol/emol
