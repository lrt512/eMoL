#!/bin/bash

GREEN='\033[1;32m'
RESET='\033[0m'

system_dependencies() {
    echo -e "\n"
    echo -e "Installing dependencies..."
    apt-get update
    apt-get install -y \
        awscli nginx certbot \
        git python3-venv python3-pip \
        python3-certbot-nginx

    apt-get install -y --no-install-recommends \
        build-essential pkg-config  \
        python3-dev \
        libmysqlclient-dev
}

python_setup() {
    pip install -U pip setuptools wheel poetry
}

echo -e "\n"
echo -e "${GREEN}System bootstrap${RESET}"

system_dependencies
python_setup

echo -e "\n"
echo -e "${GREEN}System bootstrap complete${RESET}"