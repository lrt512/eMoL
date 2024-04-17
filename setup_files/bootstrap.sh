#!/bin/bash

GREEN='\033[1;32m'
RESET='\033[0m'


# create is_dev based on existence of EMOL_DEV envvar
# Which should only be set in the docker-compose file
if [[ -z "${EMOL_DEV}" ]]; then
    is_dev=false
    SOURCE_DIR=$(dirname "$(pwd)")
else
    is_dev=true
    SOURCE_DIR="/opt/emol"
    echo -e "\n"
    echo -e "${GREEN}Dev environment${RESET}"
    echo -e "\n"
fi

install_emol() {
    # Define the source and destination directories
    if [ "$is_dev" = true ]; then
        # In the dev environment, the code is mounted to /opt/emol
        return
    fi

    INSTALL_DIR="/opt/emol"

    # Define an array of files and directories to be copied
    FILES_TO_COPY=(
        "LICENSE"
        "README.md"
        "emol/"
        "poetry.lock"
        "poetry.toml"
        "pyproject.toml"
    )

    mkdir -p "$INSTALL_DIR"

    for item in "${FILES_TO_COPY[@]}"
    do
        cp -R "$SOURCE_DIR/$item" "$INSTALL_DIR"
    done
}


cleanup_build() {
    echo -e "\n"
    echo -e "Removing build dependencies..."
    apt-get purge --auto-remove -y build-essential
    apt-get clean
    rm -rf /var/lib/apt/lists/*
}

system_dependencies() {
    echo -e "\n"
    echo -e "Installing dependencies..."
    apt-get update
    apt-get install -y \
        nginx certbot \
        git python3-venv python3-pip \
        python3-certbot-nginx

    apt-get install -y --no-install-recommends \
        build-essential pkg-config  \
        python3-dev \
        libmysqlclient-dev
}

what_even_do_we_call_this() {
    if [ "$is_dev" = true ]; then
        # We'll also need to create a .env_dev file so we can get the
        # environment variables for the dev environment in the init script
        output_file="/opt/emol/.env_dev"
        env_vars="DJANGO_SETTINGS_MODULE DB_HOST DB_NAME DB_USER DB_PASSWORD"
        echo "" > $output_file
        for var in $env_vars; do
            echo "export $var=${!var}" >> $output_file
        done
    else
        # In the real world, www-data needs to own the files    
        chown -R www-data:www-data /opt/emol
    fi
}

emol_dependencies() {
    mkdir /opt/venv
    pip install -U pip setuptools wheel poetry
    poetry install --no-dev
    chown -R www-data:www-data /opt/venv
}

configure_nginx() {
    echo -e "\n"
    echo -e "Configuring nginx..."
    rm -f /etc/nginx/sites-enabled/default
    cp ${SOURCE_DIR}/setup_files/configs/nginx.conf /etc/nginx/sites-enabled/
    update-rc.d nginx defaults
}

configure_emol() {
    echo -e "\n"
    echo -e "Configuring emol service..."
    cp ${SOURCE_DIR}/setup_files/configs/emol /etc/init.d/
    chmod +x /etc/init.d/emol
    update-rc.d emol defaults
}


system_dependencies
emol_dependencies
install_emol
what_even_do_we_call_this
# cleanup_build
configure_nginx
configure_emol

echo -e "\n"
echo -e "${GREEN}Bootstrap complete${RESET}"
