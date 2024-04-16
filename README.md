# Installation and Configuration

## Basic installation and system setup
* Clone the repository
* Enter the `setup_files` directory
* Ensure the script files are executable: chmod +x *.sh
* Run the `setup.sh` script

## Configure the database
* 

## Configure eMoL
* In `/opt/emol/emol/settings` make a copy of `sample_settings.py`:
```
cp sample_settings.py settings.py
```
* Edit `settings.py` with a text editor
  * Change the value of `BASE_URL` to the URL you will use
  * Set the value of TIME_ZONE for your locale
  * Configure the google `client_id` and `client_secret`
  

  0  3   * * *   ubuntu /opt/emol/.venv/bin/python /opt/emol/emol/manage.py send_reminders
0  4   * * *   ubuntu /opt/emol/.venv/bin/python /opt/emol/emol/manage.py clean_expired