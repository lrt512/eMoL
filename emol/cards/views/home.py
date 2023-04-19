# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from cards.mail import send_card_url, send_info_update, send_privacy_policy
from cards.models import Combatant, UpdateCode
from cards.utility.throttle import throttle
from current_user import get_current_user

logger = logging.getLogger("cards")


def index(request):
    context = {
        "current_user": get_current_user(),
    }
    return render(request, "home/index.html", context)


@throttle(limit=2, window=60, key="request_card")
@require_http_methods(["GET", "POST"])
def request_card(request):
    """Handle GET and POST methods for card requests."""
    if request.method == "GET":
        return render(request, "home/request_card.html")
    elif request.method == "POST":
        context = {
            "message": "If a combatant exists for this email, instructions have been sent."
        }
        email = request.POST.get("request-card-email", None)

        try:
            combatant = Combatant.objects.get(email=email)
            if combatant.accepted_privacy_policy:
                send_card_url(combatant)
            else:
                logger.error(f"Card request for {combatant} (privacy not accepted)")
                send_privacy_policy(combatant.privacy_acceptance)
        except Combatant.DoesNotExist:
            logger.error(f"Card URL request: No combatant for {email}")

        return render(request, "message/message.html", context)


@throttle(limit=2, window=60, key="update_info")
@require_http_methods(["GET", "POST"])
def update_info(request):
    """Handle GET and POST methods for info update requests."""
    if request.method == "GET":
        return render(request, "home/update_info.html")
    elif request.method == "POST":
        email = request.POST.get("update-info-email", None)
        try:
            context = {}
            combatant = Combatant.objects.get(email=email)
            if combatant.accepted_privacy_policy:
                code, created = UpdateCode.objects.get_or_create(combatant=combatant)
                if created:
                    logger.info(f"Created update code for {combatant}")
                    code.save()
                send_info_update(combatant, code)
            else:
                logger.error(f"Card request for {combatant} (privacy not accepted)")
                send_privacy_policy(combatant.privacy_acceptance)

            context["message"] = (
                "If a combatant with this email exists, "
                "an email has been sent with instructions for "
                "updating your information"
            )
        except Combatant.DoesNotExist:
            logger.warning("No combatant found with email %s", email)

        return render(request, "message/message.html", context)


def message(request):
    """Render the message view."""
    return render(request, "message/message_embed.html")
