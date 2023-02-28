# -*- coding: utf-8 -*-
"""Combatant warrant model."""
from django.db import models

from .card import Card
from .marshal import Marshal

__all__ = ["Warrant"]


class Warrant(models.Model):
    """Link a marshallate to a combatant via the appropriate card.

    Properties:
        combatant: The combatant
        marshal: The marshallate office held

    """

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="combatant_marshal", fields=["card", "marshal"]
            )
        ]

    card = models.OneToOneField(Card, on_delete=models.CASCADE)
    marshal = models.OneToOneField(Marshal, on_delete=models.CASCADE)

    def __str__(self):
        return "<Combatant Warrant: {0} => {1}.{2}".format(
            self.card.combatant.email, self.marshal.discipline.slug, self.marshal.slug
        )
