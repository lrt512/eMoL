# -*- coding: utf-8 -*-
"""Handlers for combatant administration views."""
import logging

from cards.models.authorization import Authorization
from cards.models.combatant import Combatant
from cards.models.discipline import Discipline
from cards.utility.decorators import permission_required
from current_user import get_current_user
from django.shortcuts import redirect, render

logger = logging.getLogger(__name__)


@permission_required("read_combatant_info")
def combatant_list(request):
    """Handle requests to view the user list.

    DataTables will use the combatant API to get combatant data via AJAX

    """
    return render(request, "combatant/combatant_list.html")


@permission_required("read_combatant_info")
def combatant_detail(request):
    """Render the combatant detail form.

    A subsequent GET to /api/combatant/<uuid> should follow to populate

    """
    context = {
        "user": get_current_user(),
        "disciplines": Discipline.objects.all(),
        "authorizations": Authorization.objects.all(),
    }
    return render(request, "combatant/combatant_detail.html", context)


'''
def combatant_stats(request):
    """Display the combatant statistics page."""
    results = {}

    for disc in Discipline.query.all():
        disc_results = []

        # Count the numbers for each authorization
        for auth in disc.authorizations:
            disc_results.append(
                {
                    "name": auth.name,
                    "count": CombatantAuthorization.query.filter(
                        CombatantAuthorization.authorization_id == auth.id
                    ).count(),
                }
            )

        # Count the numbers for each marshal type
        for marshal in disc.marshals:
            disc_results.append(
                {
                    "name": marshal.name,
                    "count": Warrant.query.filter(
                        Warrant.marshal_id == marshal.id
                    ).count(),
                }
            )

        results[disc.name] = disc_results

    return render(request, "combatant/combatant_stats.html", results=results)
'''


def combatant_card(request, card_id):
    """
    View a combatant's card, accessed by its card_id

    args:
        card_id - The ID of the card to view
    """
    try:
        combatant = Combatant.objects.get(card_id=card_id)
        if not hasattr(combatant, "waiver"):
            return render(request, "combatant/waiver_expired.html", {})

        context = {
            "legal_name": combatant.legal_name,
            "sca_name": combatant.sca_name,
            "waiver_expiry": combatant.waiver.expiry_or_expired,
            "cards": combatant.cards,
        }
        return render(request, "combatant/card.html", context)
    except Combatant.DoesNotExist:
        return redirect("/")
