# Installation and Configuration

## Basic installation and system prep
* Clone the repository
* Enter the `setup_files` directory
* Ensure the script files are executable: 
    * `chmod +x *.sh`
* Run the `setup.sh` script

## Configure Google authentication
* Go to the Google Developers Console (https://console.developers.google.com/).
* Create a new project or select an existing project.
* In the left sidebar, click on `Credentials`.
* Click on `Create credentials` and select `OAuth client ID`.
* Select `Web application` as the application type.
* Set the name for your OAuth client ID (e.g., `eMoL`).
* In the `Authorized JavaScript origins` section, add the URL of your eMoL application (e.g., `https://your-emol-url.com`).
* In the `Authorized redirect URIs` section, add the following URIs:
    * `https://your-emol-url.com/accounts/google/login/callback/`
    * `http://localhost:8000/accounts/google/login/callback/` (for local development)
    * Note: Replace `your-emol-url.com` with your actual eMoL application URL.
* Click on `Create` to generate the client ID and client secret.
* Make a note of the generated client ID and client secret.

## Configure the database
* Create a database named `emol`
* Create a user and password for eMoL to use
* Grant permissions to the eMoL user on the `emol` database

## Configure eMoL
* In `/opt/emol/emol/settings` make a copy of `sample_settings.py`:
```
cp sample_settings.py settings.py
```
* Edit `settings.py` with a text editor
* Change the value of `BASE_URL` to the URL you will use
* Set the value of `TIME_ZONE` for your locale
* Locate the `AUTHLIB_OAUTH_CLIENTS` section in settings.py.
    * Set the value of `client_id` to your Google client ID.
    * Set the value of `client_secret` to your Google client secret.
* Locate the `DATABASES` block in your `settings.py`
    * Update the block with the credentials you generated for the eMoL user
    * The sample in `sample_settings.py` is for MySQL
        * If you are using a different database, consult the [Django documentation](https://docs.djangoproject.com/en/4.2/ref/settings/#databases )
  

## Prepare the database
* Run the `db.py` script to apply migrations and collect static files

## Set up cron
* Run `setup_cron.sh` from the `setup_files` directory.
    * The script is idempotent, so you can run it multiple times without worry