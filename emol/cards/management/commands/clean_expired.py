import logging
from datetime import date

import pytz
from django.core.management.base import BaseCommand
from django.utils import timezone

from cards.models import UpdateCode
from cards.utility.time import DATE_FORMAT

logger = logging.getLogger("cards")


class Command(BaseCommand):
    help = "Send reminders for expiring Cards and Waivers."

    def handle(self, *args, **options):
        now = timezone.now().astimezone(pytz.utc)
        expired_codes = UpdateCode.objects.filter(expires_at__lte=now)
        count = expired_codes.count()
        logger.info(
            f"Clean up self-serve codes ({date.today().strftime(DATE_FORMAT)}): Found {count}"
        )

        if count == 0:
            return

        expired_codes.delete()
