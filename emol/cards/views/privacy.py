import logging

from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from cards.models.combatant import Combatant
from cards.models.privacy_policy import PrivacyPolicy

logger = logging.getLogger("cards")


@require_http_methods(["GET", "POST"])
def privacy_policy(request, code=None):
    """
    View the privacy policy, optionally with UUID for accepting it

    args:
        uuid - UUID for a PrivacyAcceptance instance
    """
    code = request.POST.get("code", code)
    try:
        combatant = Combatant.objects.get(privacy_acceptance_code=code)
    except Combatant.DoesNotExist:
        combatant = None

    context = {"policy": PrivacyPolicy.latest_text()}
    if request.method == "POST":
        if combatant is None:
            raise HttpResponseBadRequest

        if "accept" in request.POST:
            combatant.accept_privacy_policy()
            return render(request, "privacy/privacy_accepted.html", {})
        elif "decline" in request.POST:
            combatant.delete()
            return render(request, "privacy/privacy_declined.html", {})
    elif request.method == "GET":
        context["code"] = code if combatant is not None else None
        if combatant is not None:
            logger.debug(f"privacy acceptance for combatant {combatant}")

        return render(request, "privacy/privacy_policy.html", context)
