"""
ASGI config for emol project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from django.core.management.base import CommandError

if os.environ.get("DJANGO_SETTINGS_MODULE") == None:
    raise CommandError("DJANGO_SETTINGS_MODULE not set")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", None)

application = get_asgi_application()
