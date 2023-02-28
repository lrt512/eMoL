from cards.utility.date import DATE_FORMAT, add_years, today
from django.db import models

from .reminder_email import ReminderEmail


class Waiver(models.Model):
    combatant = models.OneToOneField("Combatant", on_delete=models.CASCADE)
    date_signed = models.DateField(null=False, blank=False)

    WAIVER_VALIDITY_YEARS = 7

    def __str__(self) -> str:
        return f"<Waiver: {self.combatant.name} expires {self.expiration_date}"

    @property
    def expiration_date(self):
        """Get the combatant's authorization card expiry date.

        That is, the self.card + CARD_DURATION years

        Returns:
            Date of the card's expiry date as a string

        """
        return add_years(self.date_signed, 7)

    @property
    def expiry_days(self):
        """Number of days until this combatan't waiver expires."""
        return (self.expiration_date - today()).days

    @property
    def is_valid(self) -> bool:
        return self.expiry_days > 0

    @property
    def expiry_or_expired(self):
        """Return the expiration date or EXPIRED"""
        return (
            self.expiration_date.strftime(DATE_FORMAT) if self.is_valid else "EXPIRED"
        )

    def renew(self, date_signed=None):
        """Renew combatant's waiver.

        Args:
            date_signed: Optional waiver date. If not specified, defaults to today

        """
        self.date_signed = date_signed or today()
        self.save()

        # Remove all existing ReminderEmail objects
        ReminderEmail.objects.filter(waiver=self).delete()

        # Create reminders for the 60, 30, and 14 days before expiration
        for days_before_expiry in [60, 30, 14]:
            ReminderEmail.create_for_waiver(self, days_before_expiry)

        # And create an expiry reminder
        ReminderEmail.create_for_waiver(self, 0)
