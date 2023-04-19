import logging
from datetime import timedelta

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

logger = logging.getLogger("cards")


class Reminder(models.Model):
    """Scheduled reminders for cards and waivers"""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    days_to_expiry = models.PositiveIntegerField()
    due_date = models.DateField()

    class Meta:
        unique_together = ("content_type", "object_id", "days_to_expiry")

    def __str__(self):
        s = (
            "expiry"
            if self.days_to_expiry == 0
            else f"{self.days_to_expiry} day reminder"
        )
        return f"<{self.content_object.__class__.__name__}: {self.content_object.combatant.name} - {s}>"

    @classmethod
    def create_or_update_reminders(cls, instance):
        content_type = ContentType.objects.get_for_model(instance)
        logger.info("Update reminders for %s", instance)

        # Delete existing reminders
        cls.objects.filter(content_type=content_type, object_id=instance.id).delete()

        # Create new reminders
        for days in settings.REMINDER_DAYS:
            due_date = instance.expiration_date - timedelta(days=days)
            cls.objects.create(
                content_type=content_type,
                object_id=instance.id,
                days_to_expiry=days,
                due_date=due_date,
            )

    @property
    def should_send_email(self) -> bool:
        combatant = self.content_object.combatant
        if not combatant.accepted_privacy_policy:
            return False
        return True

    def send_email(self):
        """Send the appropriate email for this reminder

        If successful, mark this reminder as sent
        """
        if not self.should_send_email:
            logger.info("Not sending reminder for %s", self)
            return

        model = self.content_type.model_class()
        try:
            sent = False
            if self.days_to_expiry == 0:
                sent = self.content_object.send_expiry(self)
            else:
                sent = self.content_object.send_reminder(self)

            if sent:
                logger.debug("Delete reminder %s", self)
                self.delete()
        except model.DoesNotExist:
            logger.error("%s instance for ID %s does not exist", model, self.object_id)
            return False
