import logging

from cards.models.card import Card
from cards.models.combatant import Combatant
from cards.models.combatant_warrant import CombatantWarrant
from cards.models.discipline import Discipline
from cards.models.marshal import Marshal
from cards.utility.date import today
from django.core.exceptions import ValidationError
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class CombatantWarrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = CombatantWarrant
        fields = ["card", "marshal", "uuid"]


logger = logging.getLogger(__name__)


class CombatantWarrantViewSet(GenericViewSet):
    """
    API endpoint to add and remove warrants from a combatant card
    """

    lookup_field = "uuid"

    queryset = CombatantWarrant.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """
        Add an warrant to a combatant's card for a discipline
        If the card doesn't exist for the specified discipline, create one.

        POST data:
            uuid - Combatant UUID
            discipline - A discipline slug
            marshal - A marshal slug
        """
        data = request.data
        uuid = data.get("combatant_uuid")
        discipline_slug = data.get("discipline")
        marshal_slug = data.get("marshal")

        logger.debug(
            "Add warrant %s/%s card for combatant %s",
            discipline_slug,
            marshal_slug,
            uuid,
        )

        try:
            combatant = Combatant.objects.get(uuid=uuid)
        except Combatant.DoesNotExist:
            return Response(
                f"Combatant {uuid} not found", status=status.HTTP_404_NOT_FOUND
            )

        try:
            discipline = Discipline.objects.get(slug=discipline_slug)
        except Discipline.DoesNotExist:
            return Response(
                f"No such discipline '{discipline_slug}'",
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            marshal = (
                Marshal.objects.filter(discipline=discipline)
                .filter(slug=marshal_slug)
                .get()
            )
        except Marshal.DoesNotExist:
            return Response(
                f"No such warrant '{marshal_slug}'", status=status.HTTP_404_NOT_FOUND
            )

        try:
            card = (
                Card.objects.filter(discipline=discipline)
                .filter(combatant=combatant)
                .get()
            )
        except Card.DoesNotExist:
            card = None

        if card is None:
            logger.debug("Create %s card for combatant %s", discipline_slug, uuid)
            card = Card(combatant=combatant, discipline=discipline, card_date=today())
            card.save()

        logger.debug("Create combatant-warrant ,record for combatant %s", uuid)
        serializer = CombatantWarrantSerializer(
            data={"card": card.id, "marshal": marshal.id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, uuid):
        """
        Delete the given CombatantWarrant
        If the related card has no warrants left, delete that too
        """
        try:
            instance = CombatantWarrant.objects.get(uuid=uuid)
        except CombatantWarrant.DoesNotExist:
            return Response(
                f"No such combatant-warrant {uuid}", status=status.HTTP_404_NOT_FOUND
            )
        except ValidationError as exc:
            return Response(f"{exc}", status=status.HTTP_404_NOT_FOUND)

        logger.debug("Remove combatant-warrant %s", uuid)
        card = instance.card
        instance.delete()

        if card.authorizations.count() == 0 and card.warrants.count() == 0:
            logger.debug(
                "Card has no more authorizations or warrants attached, removing card"
            )
            card.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
