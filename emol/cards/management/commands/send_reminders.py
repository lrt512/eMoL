from django.core.management.base import BaseCommand
from django.utils import timezone

from emailer import Emailer

from cards.models.reminder import Reminder


class Command(BaseCommand):
    help = "Send reminders for expiring Cards and Waivers."

    def handle(self, *args, **options):
        due_reminders = Reminder.objects.filter(due_date__lte=timezone.now().date())
        count = due_reminders.count()
        self.stdout.write(self.style.SUCCESS(f"Found {count} reminders to send"))

        if count == 0:
            return

        for reminder in due_reminders:
            if reminder.should_send_email:
                if reminder.send_email():
                    reminder.delete()

        self.stdout.write(self.style.SUCCESS("Reminders sent"))
