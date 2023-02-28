from datetime import timedelta

from cards.mail import (
    send_card_expiry,
    send_card_reminder,
    send_waiver_expiry,
    send_waiver_reminder,
)
from django.db import models


class ReminderEmail(models.Model):
    """Scheduled reminders for cards and waivers"""

    card = models.ForeignKey("Card", on_delete=models.CASCADE, null=True, blank=True)
    waiver = models.ForeignKey(
        "Waiver", on_delete=models.CASCADE, null=True, blank=True
    )
    reminder_date = models.DateField()
    is_expiration = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)

    def __str__(self) -> str:
        combatant = self.card.combatant if self.card else self.waiver.combatant
        return f"{'Card' if self.card else 'Waiver'} {'expiry' if self.is_expiration else 'reminder'}: {combatant.email} ({self.reminder_date})"

    def clean(self):
        if self.card and self.waiver:
            raise models.ValidationError(
                "ReminderEmail has a card or a waiver, not both."
            )

    @classmethod
    def create_for_card(cls, card, days_before_expiry):
        """Create an instance for a card"""
        reminder_date = card.expiration_date + timedelta(days=-days_before_expiry)
        return cls.objects.create(
            card=card,
            reminder_date=reminder_date,
            is_expiration=(days_before_expiry == 0),
        )

    @classmethod
    def create_for_waiver(cls, waiver, days_before_expiry):
        """Create an instance for a waiver"""
        reminder_date = waiver.expiration_date + timedelta(days=-days_before_expiry)
        return cls.objects.create(
            waiver=waiver,
            reminder_date=reminder_date,
            is_expiration=(days_before_expiry == 0),
        )

    def send_email(self):
        """Send the appropriate email for this reminder

        If successful, mark this reminder as sent
        """
        if self.card is not None:
            if self.is_expiration:
                self.sent = send_card_expiry(self)
            else:
                self.sent = send_card_reminder(self)
        else:
            if self.is_expiration:
                self.sent = send_waiver_expiry(self)
            else:
                self.sent = send_waiver_reminder(self)

        if self.sent:
            self.save()
