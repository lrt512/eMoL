FROM ubuntu:22.04

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Toronto

COPY setup_files/bootstrap_system.sh /tmp
RUN chmod +x /tmp/bootstrap_system.sh
RUN /tmp/bootstrap_system.sh

# Fake AWS credentials for Localstack
RUN aws configure set default.region ca-central-1 && \
    aws configure set default.output json && \
    aws configure set aws_access_key_id fake_access_key && \
    aws configure set aws_secret_access_key fake_secret_key

EXPOSE 80
WORKDIR /opt/emol/emol
