from uuid import uuid4

from django.db import models

from .authorization import Authorization
from .card import Card


class CombatantAuthorization(models.Model):
    """
    Model for the through table between Card and Authorization.
    Declared in the Card model's authorization attribute.
    """

    class Meta:
        db_table = "cards_combatant_authorization"
        indexes = [models.Index(fields=["uuid"])]

    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    authorization = models.ForeignKey(Authorization, on_delete=models.DO_NOTHING)
    uuid = models.UUIDField(default=uuid4, editable=False)

    def __str__(self):
        return f"<Authorization: {self.card.combatant.name}/{self.authorization.name} ({self.card.discipline.name})"
