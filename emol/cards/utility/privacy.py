from urllib.parse import urljoin

from django.conf import settings
from django.urls import reverse


def privacy_policy_url(combatant):
    """Generate the URL for a user to visit to accept the privacy policy.

    Uses the uuid member to uniquely identify this privacy accepted record,
    and through it the combatant.

    Returns:
        String containing the URL

    """
    return urljoin(
        settings.BASE_URL,
        reverse("privacy-policy", args=[combatant.privacy_acceptance_code]),
    )
