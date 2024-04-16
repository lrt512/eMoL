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
else
    cp -R ../emol /opt
    chown -R www-data:www-data /opt/emol
    SOURCE_DIR=`pwd`
fi

pip install --upgrade pip
pip install wheel
pip install -r ${SOURCE_DIR}/requirements/prod.txt

chown -R www-data:www-data /opt/venv

rm /etc/nginx/sites-enabled/default
cp ${SOURCE_DIR}/setup_files/nginx.conf /etc/nginx/sites-enabled/

apt-get purge --auto-remove -y build-essential
apt-get clean
rm -rf /var/lib/apt/lists/*

service nginx start

cp ${SOURCE_DIR}/setup_files/emol /etc/init.d/
chmod +x /etc/init.d/emol

# Set nginx and emol to both start on boot
update-rc.d emol defaults
update-rc.d nginx defaults

echo -e "${GREEN}Setup complete${RESET}"
echo -e "\n"
echo -e "Next: Configure the database and eMol"
echo -e "See the README for more information"


echo -e "Then run the following commands:"
echo -e "\n"
echo -e "service emol start"
echo -e "service nginx restart"
echo -e "\n"
echo -e "Finally, run certbot to get an SSL certificate"
echo -e "certbot --nginx"
