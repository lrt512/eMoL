"""Base settings for production deployment"""
import os
import boto3


from .defaults import *  # noqa: F403, F401

# -------------------------------------------------------------------------------------
# !!! Configure these settings for your deployment

AWS_REGION = "ca-central-1"

# This is the secret key for your Django application. It should be a long
# random string. It is used for cryptographic signing. Keep it secret!
# Here are some possible ways to handle it:
SECRET_KEY = "!!! REPLACE WITH A LONG RANDOM STRING !!!"
# - or -
# SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
# - or -
# from . import get_parameter
# ssm_client = boto3.client("ssm", region_name="ca-central-1")
# SECRET_KEY = get_parameter("/emol/secret_key", ssm_client)

# This is the base URL for your site. It is whatever you have configured
# in your web server to point to the Django application. For example, if
# you have configured your web server to point to the Django application
# at http://yourdomain.com, then this should be "http://yourdomain.com".
# If it's at http://yourdomain.com/emol, then this should be
# "http://yourdomain.com/emol".
# If it's a subdomain like http://emol.yourdomain.com, then this should be
# "http://emol.yourdomain.com".
BASE_URL = "http://yourdomain.com"

# Timezone identifier for your locale
# See https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
TIME_ZONE = "America/Toronto"

# Address that emails are sent from. This is what will show up in the
# "From" field of the email. This should be an email address that is
# configured to send email from your server. If you are using a service
# like AWS SES, then this must be an email address that is verified
# in SES.
MAIL_DEFAULT_SENDER = "emol@kingdom.org"

# Email address for your kingdom MOL
MOL_EMAIL = "mol@kingdom.org"

# Configure Google authentication
AUTHLIB_OAUTH_CLIENTS = {
    "google": {
        "client_id": "!!! REPLACE WITH YOUR GOOGLE OAUTH CLIENT ID !!!",
        "client_secret": "!!! REPLACE WITH YOUR GOOGLE OAUTH CLIENT SECRET !!!",
    }
}

# Configure your database. This is for MySQL
# See https://docs.djangoproject.com/en/4.2/ref/settings/#databases for others
#
# Typical settings for MySQL
#   "NAME": "emol",
#   "USER": "emol_db_user",
#   "HOST": "https://db.example.com",
#
# For the database password, if you can inject it into the environment
# that is a best practice. If you can't, you can put it here like
# below but be sure to keep it secret.
# DATABASE_PASSWORD = "your_password"
DATABASE_PASSWORD = os.getenv("EMOL_DB_PASSWORD")
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "YOUR_DATABASE_NAME",
        "USER": "YOUR_DATABASE_USER",
        "PASSWORD": DATABASE_PASSWORD,
        "HOST": "YOUR_DATABASE_HOST",
        "PORT": "3306",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            "charset": "utf8mb4",
        },
    }
}

# !!! End of settings to configure
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# !!! Default values that can be changed if desired
# These are the default values for various things that you
# can change if you want.

# Number of days before expiry for reminder emails
REMINDER_DAYS = [60, 30, 14, 0]

# Global throttle config
# This is for limiting the effect of a DDOS attack or web crawlers
# that are hitting the site too hard. It will limit the number of
# requests that can be made in a given window of time.
# The default is 20 requests in 1 hour.
# Don't set it so tight that it affects normal users!
# But also note that authenticated users are not throttled.
GLOBAL_THROTTLE_LIMIT = 20
GLOBAL_THROTTLE_WINDOW = 3600

# If you're not using AWS SES, you'll need to write your own emailer.
# If you are using AWS SES, make sure AWS_REGION is set to your region.
EMAILER = "emol.emailer.AWSEmailer"
AWS_REGION = "ca-central-1"

# !!! End of settings that can be changed
# -------------------------------------------------------------------------------------





