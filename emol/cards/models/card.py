# -*- coding: utf-8 -*-
"""Model an authorization card.

    A card represents a single martial discipline.

    Card
    |
    - Discipline (via discipline_id)
    |
    - Authorizations (Authorization model via CombatantAuthorization)
    |
    - Warrants (Marshal model via Warrant)
    |
    - Card Date (The date auths were renewed, not the expiry date)

    A combatant may hold one card for each discipline they have authorizations
    in. These show up as the `cards` relationship on the Combatant model.
"""

import logging
from uuid import uuid4

from cards.utility.date import DATE_FORMAT, add_years, today
from django.db import models

from .authorization import Authorization
from .discipline import Discipline
from .marshal import Marshal
from .reminder_email import ReminderEmail

from cards.utility.named_tuples import NameSlugTuple

__all__ = ["Card"]

logger = logging.getLogger(__name__)


class Card(models.Model):
    """Model an authorization card

    Card date is the date that the card was renewed.
    The card_expiry property gives the expiry date

    Discipline will be none if card date is global

    Attributes:
        id: Primary key in the database
        combatant_id: The combatant's id
        discipline_id: ID of the discipline this card is for
        card_issued: Date this card was last renewed
        authorizations: Authorizations attached to this card
            (Authorization model via CombatantAuthorization)
        warrants: Marshal warrants attached to this card
            (Marshal model via Warrant)

    Properties:
        expiration_date: The card's expiration date
        expiry_days: Number of days until expiry

    Backrefs:
        reminders: This card's expiry reminders
    """

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="combatant_card", fields=["combatant", "discipline"]
            )
        ]

    combatant = models.ForeignKey(
        "Combatant", on_delete=models.CASCADE, related_name="cards"
    )
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    authorizations = models.ManyToManyField(
        Authorization, through="CombatantAuthorization"
    )
    warrants = models.ManyToManyField(Marshal, through="CombatantWarrant")
    uuid = models.UUIDField(default=uuid4)

    card_issued = models.DateField()

    def __str__(self) -> str:
        return f"<Card: {self.combatant.sca_name}/{self.discipline.name}>"

    @property
    def expiration_date(self):
        """Get the combatant's authorization card expiry date.

        That is, the self.card + CARD_DURATION years

        Returns:
            Date of the card's expiry date as a string

        """
        return add_years(self.card_issued, 2)

    @property
    def expiry_or_expired(self):
        """Return the expiration date or EXPIRED"""
        return (
            self.expiration_date.strftime(DATE_FORMAT) if self.is_valid else "EXPIRED"
        )

    @property
    def is_valid(self) -> bool:
        """Card is not past its expiration date"""
        return self.expiry_days > 0

    @property
    def expiry_days(self):
        """Number of days until this card expires."""
        return (self.expiration_date - today()).days

    def renew(self, renew_date=None):
        """Renew this card with a new card_date

        Fix up the reminders associated with this card, too.
        """
        self.card_issued = renew_date or today()
        self.save()

        # Remove all existing ReminderEmail objects
        ReminderEmail.objects.filter(card=self).delete()

        # Create reminders for the 60, 30, and 14 days before expiration
        for days_before_expiry in [60, 30, 14]:
            ReminderEmail.create_for_card(self, days_before_expiry)

        # And create an expiry reminder
        ReminderEmail.create_for_card(self, 0)

    def has_authorization(self, authorization):
        """Does this card have a given authorization?"""
        try:
            a = Authorization.find(self.discipline, authorization)
            return a in self.authorizations.all()
        except Authorization.DoesNotExist:
            return False

    def has_warrant(self, marshal):
        """Does this card have a given marshal warrant?"""
        try:
            m = Marshal.find(self.discipline, marshal)
            return m in self.warrants.all()
        except Marshal.DoesNotExist:
            return False

    @property
    def card_ordered_authorizations(self):
        """
        Model ordering can be a bit wonky, so let's
        1 - split out into lists of primary and secondary auths
        2 - sort those lists in place on name
        3 - return them combined

        We'll also return NamedTuples rather than objects for convenience
        """
        auths = self.discipline.authorizations.all()
        primary = [
            NameSlugTuple(name=a.name, slug=a.slug) for a in auths if a.is_primary
        ]
        secondary = [
            NameSlugTuple(name=a.name, slug=a.slug) for a in auths if not a.is_primary
        ]
        return sorted(primary, key=lambda x: x.name) + sorted(
            secondary, key=lambda x: x.name
        )

    @property
    def card_ordered_marshals(self):
        """
        Model ordering can be a bit wonky, so let's just sort our marshal types
        alphabetically and return

        We'll also return NamedTuples rather than objects for convenience
        """
        marshals = self.discipline.marshals.all()
        tuples = [NameSlugTuple(name=m.name, slug=m.slug) for m in marshals]
        return tuples
