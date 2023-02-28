import logging

from cards.models.card import Card
from cards.models.combatant import Combatant
from cards.models.discipline import Discipline
from cards.models.combatant_authorization import CombatantAuthorization
from cards.models.combatant_warrant import CombatantWarrant
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import GenericViewSet

from .permissions import CardDatePermission

logger = logging.getLogger(__name__)


class CardSerializer(ModelSerializer):
    """Serializer for Card model"""

    class Meta:
        model = Card
        fields = ["discipline", "authorizations", "warrants"]


class CardViewSet(GenericViewSet):
    """
    API viewset that retrieves card data for combatants
    """

    queryset = Card.objects.all()
    serializer_class = Card
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated]
    lookup_field = "uuid"

    def retrieve(self, request, uuid):
        """
        Handle GET requests

        params:
            uuid - A combatant's UUID
        """
        cards = Card.objects.filter(combatant__uuid=uuid)
        data = []
        for card in cards.all():
            card_data = {
                "discipline": card.discipline.slug,
                "card_issued": card.card_issued,
                "uuid": card.uuid,
            }

            auth_data = []
            for auth in CombatantAuthorization.objects.filter(card=card).all():
                auth_data.append(
                    {
                        "authorization": auth.authorization.slug,
                        "uuid": auth.uuid,
                    }
                )
            card_data["authorizations"] = auth_data

            warrant_data = []
            for warrant in CombatantWarrant.objects.filter(card=card).all():
                warrant_data.append(
                    {
                        "marshal": warrant.marshal.slug,
                        "uuid": warrant.uuid,
                    }
                )
            card_data["warrants"] = warrant_data

            data.append(card_data)

        return Response(status=status.HTTP_200_OK, data=data)


class CardDateSerializer(serializers.Serializer):
    """Serializer for card issue date updates"""

    uuid = serializers.UUIDField()
    discipline_slug = serializers.CharField()
    card_issued = serializers.DateField()

class CardDateViewSet(GenericViewSet):
    """
    API viewset to add and remove auths from a combatant card
    """

    queryset = Card.objects.all()
    permission_classes = [CardDatePermission]
    serializer_class = CardDateSerializer
    renderer_classes = [JSONRenderer]

    def _update_card_issued_date(self, request_data):
        """
        Add card date to a combatant's card
        If the card doesn't exist for the specified discipline, create one.

        POST data:
            uuid - Combatant UUID
            discipline - A discipline slug
            card_issued - Card's new issue date
        """
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        
        uuid = serializer.data.get("uuid")
        discipline_slug = serializer.data.get("discipline_slug")
        card_issued = serializer.data.get("card_issued")

        logger.debug(
            "Update card issue date on %s card for combatant %s",
            discipline_slug,
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
            card = (
                self.queryset.filter(discipline=discipline)
                .filter(combatant=combatant)
                .get()
            )
        except Card.DoesNotExist:
            logger.debug("Create %s card for combatant %s", discipline_slug, uuid)
            card = Card(
                combatant=combatant, discipline=discipline, card_issued=card_issued
            )
        finally:
            card.card_issued = card_issued
            card.save()

    def update(self, request, **kwargs):
        """PUT endpoint for _update_card_issued_date
        
        A bit janky on HTTP verbs since we will create a card if it 
        doesn't exist. But... meh. It's all an "update"
        """
        self._update_card_issued_date(request.data)
        return Response(status=status.HTTP_204_NO_CONTENT)
