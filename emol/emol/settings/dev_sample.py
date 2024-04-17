import os

from .defaults import *  # noqa: F401, F403

# Sample settings for development environment settings.
# Copy this file and customize it for your development environment
# If you copy it to dev.py, it will not be checked into version control
# See sample_settings.py for more information on these settings

AWS_REGION = "ca-central-1"

BASE_URL = "http://localhost:8000"
SECRET_KEY = "super-secret-development-key-1234"

DEBUG = True
NO_ENFORCE_PERMISSIONS = True
ALLOWED_HOSTS = ["localhost"]

# Configure Google authentication
AUTHLIB_OAUTH_CLIENTS = {
    "google": {
        "client_id": "!!! REPLACE WITH YOUR GOOGLE OAUTH CLIENT ID !!!",
        "client_secret": "!!! REPLACE WITH YOUR GOOGLE OAUTH CLIENT SECRET !!!",
    }
}

TIME_ZONE = "America/Toronto"

# email stuff
SEND_EMAIL = False
MAIL_DEFAULT_SENDER = "emol@kingdom.org"
MOL_EMAIL = "minister.of.lists@kingdom.org"

# Reminders app config
REMINDER_DAYS = [60, 30, 14, 0]

# Global throttle config
GLOBAL_THROTTLE_LIMIT = 20000
GLOBAL_THROTTLE_WINDOW = 3600

# The docker-compose file sets these environment variables
# So it will Just Work(TM) when you run `docker-compose up`
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": os.environ.get("DB_HOST"),
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
    },
    "cache_db": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": os.environ.get("DB_HOST"),
        "NAME": f"{os.environ.get('DB_NAME')}_cache",
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
    },
}

# Security config
CORS_ORIGIN_WHITELIST = [
    "http://localhost",
]
