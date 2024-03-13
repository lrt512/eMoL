"""Base settings for production deployment"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

BASE_URL = "http://localhost:8000"

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

DEBUG = False
NO_ENFORCE_PERMISSIONS = False

ALLOWED_HOSTS = ["localhost"]

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
STATIC_ROOT = "/app/static/"

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
                "%(asctime)s [%(levelname)-8s] " "(%(module)s.%(funcName)s) %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "emol",
        "USER": "emol_db_user",
        "PASSWORD": os.getenv("EMOL_DB_PASSWORD"),
        "HOST": "localhost",
        "PORT": "3306",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            "charset": "utf8mb4",
        },
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "emol_cache",
    }
}

CACHE_TTL = 60 * 15  # 15 minutes
LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/Toronto"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Authentication config
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

AUTH_USER_MODEL = "sso_user.SSOUser"
AUTHLIB_OAUTH_CLIENTS = {
    "google": {
        "client_id": "!!! REPLACE WITH YOUR GOOGLE OAUTH CLIENT ID !!!",
        "client_secret": "!!! REPLACE WITH YOUR GOOGLE OAUTH CLIENT SECRET !!!",
    }
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ]
}

# AWS Stuff
AWS_REGION = "ca-central-1"

# email stuff
SEND_EMAIL = False
MAIL_DEFAULT_SENDER = "ealdormere.emol@gmail.com"

# Kingdom stuff
MOL_EMAIL = "ealdormere.mol@gmail.com"

# Reminders app config
REMINDER_DAYS = [60, 30, 14, 0]

# Global throttle config
GLOBAL_THROTTLE_LIMIT = 20
GLOBAL_THROTTLE_WINDOW = 3600

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
