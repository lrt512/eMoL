import logging

from cards.models.authorization import Authorization
from cards.models.card import Card
from cards.models.combatant import Combatant
from cards.models.combatant_authorization import CombatantAuthorization
from cards.models.discipline import Discipline
from cards.utility.date import today
from django.core.exceptions import ValidationError
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

logger = logging.getLogger(__name__)


class CombatantAuthorizationSerializer(serializers.ModelSerializer):
    """Serializer for CombatantAuthorization model"""

    class Meta:
        model = CombatantAuthorization
        fields = ["card", "authorization", "uuid"]


class CombatantAuthorizationViewSet(GenericViewSet):
    """
    API viewset to add and remove auths from a combatant card
    """

    lookup_field = "uuid"

    queryset = CombatantAuthorization.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """
        Add an authorization to a combatant's card for a discipline
        If the card doesn't exist for the specified discipline, create one.

        POST data:
            uuid - Combatant UUID
            discipline - A discipline slug
            authorization - An authorization slug
        """
        data = request.data
        uuid = data.get("combatant_uuid")
        discipline_slug = data.get("discipline")
        authorization_slug = data.get("authorization")

        logger.debug(
            "Add authorization %s/%s card for combatant %s",
            discipline_slug,
            authorization_slug,
            uuid,
        )

        try:
            combatant = Combatant.objects.get(uuid=uuid)
        except Combatant.DoesNotExist:
            return Response("Combatant not found", status=status.HTTP_404_NOT_FOUND)

        try:
            discipline = Discipline.objects.get(slug=discipline_slug)
        except Discipline.DoesNotExist:
            return Response(
                f"No such discipline '{discipline_slug}'",
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            authorization = (
                Authorization.objects.filter(discipline=discipline)
                .filter(slug=authorization_slug)
                .get()
            )
        except Authorization.DoesNotExist:
            return Response(
                f"No such authorization '{authorization_slug}'",
                status=status.HTTP_404_NOT_FOUND,
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
            card = Card(combatant=combatant, discipline=discipline, card_issued=today())
            card.save()

        logger.debug("Create combatant-authorization record")
        serializer = CombatantAuthorizationSerializer(
            data={"card": card.id, "authorization": authorization.id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, uuid):
        """
        Delete the given CombatantAuthorization
        If the related card has no authorizations left, delete that too
        """
        try:
            instance = CombatantAuthorization.objects.get(uuid=uuid)
        except CombatantAuthorization.DoesNotExist:
            return Response(
                f"No such combatant-authorization {uuid}",
                status=status.HTTP_404_NOT_FOUND,
            )
        except ValidationError as exc:
            return Response(f"{exc}", status=status.HTTP_404_NOT_FOUND)

        logger.debug("Remove combatant-authorization %s", uuid)
        card = instance.card
        instance.delete()

        if card.authorizations.count() == 0 and card.warrants.count() == 0:
            logger.debug(
                "Card has no more authorizations or warrants attached, removing card"
            )
            card.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
