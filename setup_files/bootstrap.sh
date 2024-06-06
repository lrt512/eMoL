#!/bin/bash

GREEN='\033[1;32m'
RESET='\033[0m'

EMOL_DIR=/opt/emol

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

environment_specific_setup() {
    if [ "$is_dev" = true ]; then
        # We'll also need to create a .env_dev file so we can get the
        # environment variables for the dev environment in the init script
        # output_file="/opt/emol/.env_dev"
        # env_vars="DJANGO_SETTINGS_MODULE DB_HOST DB_NAME DB_USER DB_PASSWORD"
        # echo "" > $output_file
        # for var in $env_vars; do
        #     echo "export $var=${!var}" >> $output_file
        # done

        aws ssm put-parameter --name "/emol/django_settings_module" --value "emol.settings.dev" --type "SecureString" --endpoint-url "http://localstack:4566"
        aws ssm put-parameter --name "/emol/oauth_client_id" --value "$OAUTH_CLIENT_ID" --type "SecureString" --endpoint-url "http://localstack:4566"
        aws ssm put-parameter --name "/emol/oauth_client_secret" --value "$OAUTH_CLIENT_SECRET" --type "SecureString" --endpoint-url "http://localstack:4566"
        aws ssm put-parameter --name "/emol/db_host" --value "db" --type "SecureString" --endpoint-url "http://localstack:4566"
        aws ssm put-parameter --name "/emol/db_name" --value "emol" --type "SecureString" --endpoint-url "http://localstack:4566"
        aws ssm put-parameter --name "/emol/db_user" --value "emol_db_user" --type "SecureString" --endpoint-url "http://localstack:4566"
        aws ssm put-parameter --name "/emol/db_password" --value "emol_db_password" --type "SecureString" --endpoint-url "http://localstack:4566"
    else
        # In the real world, www-data needs to own the files    
        chown -R www-data:www-data /opt/emol
    fi
}

emol_dependencies() {
    pushd /opt/emol
    poetry install --only main
    chown -R www-data:www-data /opt/emol_venv
    popd
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


install_emol
emol_dependencies
environment_specific_setup
if [ "$is_dev" = false ]; then
    # cleanup_build
    configure_nginx
    configure_emol
fi
echo -e "\n"
echo -e "${GREEN}Bootstrap complete${RESET}"
