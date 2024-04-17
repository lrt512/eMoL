"""
WSGI config for emol project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.core.management.base import CommandError

if os.environ.get("DJANGO_SETTINGS_MODULE") == None:
    raise CommandError("DJANGO_SETTINGS_MODULE not set")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", None)

application = get_wsgi_application()
