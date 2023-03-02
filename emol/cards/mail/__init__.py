import logging

from cards.utility.privacy import privacy_policy_url
from emailer import Emailer

from .email_templates import EMAIL_TEMPLATES

logger = logging.getLogger("django")


def send_waiver_expiry(reminder):
    """Send a waiver expiry notice to a combatant.

    Args:
        reminder: A ReminderEmail object
    """
    template = EMAIL_TEMPLATES.get("waiver_expiry")
    body = template.get("body").format(
        expiry_days=reminder.combatant.waiver.expiry_days,
        expiry_date=reminder.combatant.waiver.expiry_date,
    )
    return Emailer.send_email(reminder.combatant.email, template.get("subject"), body)


def send_card_reminder(reminder):
    """Send a card reminder notice to a combatant.

    Args:
        reminder: A ReminderEmail object
    """
    template = EMAIL_TEMPLATES.get("card_reminder")
    body = template.get("body").format(
        expiry_days=reminder.card.expiry_days,
        expiry_date=reminder.card.expiry_date_str,
        discipline=reminder.card.discipline.name,
    )
    return Emailer.send_email(
        reminder.card.combatant.email, template.get("subject"), body
    )


def send_card_expiry(reminder):
    """Send a card expiration notification to a combatant

    Args:
        reminder: A ReminderEmail object
    """
    template = EMAIL_TEMPLATES.get("card_expiry")
    body = template.get("body").format(
        discipline=reminder.card.discipline.name,
    )
    return Emailer.send_email(
        reminder.card.combatant.email, template.get("subject"), body
    )


def send_waiver_reminder(reminder):
    """Send a waiver reminder notice to a combatant.

    Args:
        reminder: A ReminderEmail object

    """
    template = EMAIL_TEMPLATES.get("waiver_expiry")
    body = template.get("body").format(
        expiry_days=reminder.combatant.waiver.expiry_days,
        expiry_date=reminder.combatant.waiver.expiry_date,
    )
    return Emailer.send_email(reminder.combatant.email, template.get("subject"), body)


def send_info_update(combatant, update_request):
    """Send a information update link to a combatant.

    Args:
        combatant: The combatant to send notice to
        update_request: The update request

    """
    template = EMAIL_TEMPLATES.get("info_update")
    body = template.get("body").format(update_url=update_request.change_info_url)
    return Emailer.send_email(combatant.email, template.get("subject"), body)


def send_card_url(combatant):
    """Send a combatant their card URL.

    Args:
        combatant: The combatant to send notice to

    Raises:
        PrivacyAcceptance.NotAccepted if the combatant has not
            yet accepted the privacy policy

    """
    template = EMAIL_TEMPLATES.get("card_url")
    body = template.get("body").format(card_url=combatant.card_url)
    return Emailer.send_email(combatant.email, template.get("subject"), body)


def send_privacy_policy(combatant):
    """Send the privacy policy email to a combatant.

    Use the given PrivacyAcceptance record to get the email address and
    dispatch the email.

    Args:
        privacy_acceptance: A PrivacyAcceptance object to work from

    """
    template = EMAIL_TEMPLATES.get("privacy_policy")
    body = template.get("body").format(privacy_policy_url=privacy_policy_url(combatant))
    return Emailer.send_email(combatant.email, template.get("subject"), body)
