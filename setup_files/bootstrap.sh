#!/bin/bash

GREEN='\033[1;32m'
RESET='\033[0m'

# create is_dev based on existence of EMOL_DEV envvar
if [[ -z "${EMOL_DEV}" ]]; then
    is_dev=false
else
    is_dev=true
    echo -e "\n"
    echo -e "${GREEN}Dev environment${RESET}"
    echo -e "\n"
fi

apt-get update
apt-get install -y \
    nginx certbot \
    git python3-venv python3-pip \
    python3-certbot-nginx

apt-get install -y --no-install-recommends \
    build-essential pkg-config  \
    python3-dev \
    libmysqlclient-dev

mkdir -p /opt/venv
python3 -m venv /opt/venv
source /opt/venv/bin/activate

# dev environment via docker compose will mount the code to /mnt/emol
if [ "$is_dev" = true ]; then
    ln -s /mnt/emol/emol /opt/emol
    SOURCE_DIR=/mnt/emol

    # We'll also need to create a .env_dev file so we can get the
    # environment variables for the dev environment in the init script
    output_file="/opt/emol/.env_dev"
    env_vars="DJANGO_SETTINGS_MODULE DB_HOST DB_NAME DB_USER DB_PASSWORD"
    echo "" > $output_file
    for var in $env_vars; do
        echo "export $var=${!var}" >> $output_file
    done
else
    cp -R ../emol /opt
    chown -R www-data:www-data /opt/emol
    SOURCE_DIR=`pwd`
fi

pip install --upgrade pip
pip install wheel
pip install -r ${SOURCE_DIR}/requirements/prod.txt

chown -R www-data:www-data /opt/venv

echo -e "\n"
echo -e "Removing build dependencies..."
apt-get purge --auto-remove -y build-essential
apt-get clean
rm -rf /var/lib/apt/lists/*

echo -e "\n"
echo -e "Configuring nginx..."
rm -f /etc/nginx/sites-enabled/default
cp ${SOURCE_DIR}/setup_files/configs/nginx.conf /etc/nginx/sites-enabled/
update-rc.d nginx defaults

echo -e "\n"
echo -e "Configuring emol service..."
cp ${SOURCE_DIR}/setup_files/configs/emol /etc/init.d/
chmod +x /etc/init.d/emol
update-rc.d emol defaults

echo -e "\n"
echo -e "${GREEN}Bootstrap complete${RESET}"
