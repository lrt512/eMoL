import uuid
from datetime import datetime
from urllib.parse import urljoin

from django.conf import settings
from django.db import models
from django.urls import reverse

from cards.utility.time import utc_tomorrow

from .combatant import Combatant


class UpdateCode(models.Model):
    combatant = models.OneToOneField(Combatant, on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4, unique=True)
    expires_at = models.DateTimeField(default=utc_tomorrow)

    def __str__(self):
        return f"Update Code for {self.combatant}: {self.expires_at}"

    def is_valid(self):
        return datetime.utcnow() < self.expires_at

    @property
    def url(self):
        """The URL for this update code."""
        return urljoin(
            settings.BASE_URL, reverse("self-serve-update", args=[self.code])
        )
