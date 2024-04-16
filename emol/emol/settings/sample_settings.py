"""Base settings for production deployment"""
import os
from pathlib import Path

# -------------------------------------------------------------------------------------
# !!! Configure these settings for your deployment

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
# like AWS SES, then this should be an email address that is verified
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





# -------------------------------------------------------------------------------------
# !!!! Here be dragons, change at your own risk
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

DEBUG = False
NO_ENFORCE_PERMISSIONS = False

ALLOWED_HOSTS = ["*"]

SECURE_HSTS_SECONDS = 31536000

INSTALLED_APPS = [
    "sso_user",  # needs to be before contrib.admin
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "markdownx",
    "corsheaders",
    "cards",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "global_throttle.middleware.GlobalThrottleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "csp.middleware.CSPMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django_permissions_policy.PermissionsPolicyMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "current_user.middleware.ThreadLocalUserMiddleware",
]

ROOT_URLCONF = "emol.urls"
STATIC_URL = "static/"
STATIC_ROOT = "/opt/emol/static/"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates/"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "emol.wsgi.application"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "app",
        },
    },
    "root": {"level": "DEBUG", "handlers": ["console"]},
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
    "formatters": {
        "app": {
            "format": (
            ),
                "%(asctime)s [%(levelname)-8s] " "(%(module)s.%(funcName)s) %(message)s"
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
}


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "emol_cache",
    }
}

CACHE_TTL = 60 * 15  # 15 minutes
LANGUAGE_CODE = "en-us"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Authentication config
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

AUTH_USER_MODEL = "sso_user.SSOUser"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ]
}

# email stuff
SEND_EMAIL = True

# Security config
CORS_ORIGIN_WHITELIST = [
    "http://localhost",
]

SECURE_HSTS_SECONDS = 31536000
PERMISSIONS_POLICY = {
    "accelerometer": [],
    "autoplay": [],
    "camera": [],
    "display-capture": [],
    "encrypted-media": [],
    "fullscreen": [],
    "geolocation": [],
    "gyroscope": [],
    "magnetometer": [],
    "microphone": [],
    "midi": [],
    "payment": [],
    "usb": [],
}

CSP_IMG_SRC = ("'self'", "data:", "https://cdn.datatables.net")
CSP_FONT_SRC = (
    "'self'",
    "https://maxcdn.bootstrapcdn.com",
    "https://cdnjs.cloudflare.com",
)
CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",  # needed for datatables
    "https://cdnjs.cloudflare.com",
    "https://maxcdn.bootstrapcdn.com",
    "https://cdn.datatables.net",
)
CSP_SCRIPT_SRC = (
    "'self'",
    "https://cdnjs.cloudflare.com",
    "https://maxcdn.bootstrapcdn.com",
    "https://cdn.datatables.net",
    "sha256-PhCsD9cDmNHcYlaLal8yHa4TGyayjyPy1/u4cyvSojQ=",
)
