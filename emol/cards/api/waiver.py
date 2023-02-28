from datetime import datetime

from cards.models.combatant import Combatant
from cards.models.waiver import Waiver
from rest_framework import serializers, status, viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from .permissions import WaiverDatePermission


class WaiverSerializer(ModelSerializer):
    uuid = serializers.UUIDField(required=False)

    class Meta:
        model = Waiver
        fields = [
            "uuid",
            "date_signed",
            "expiration_date",
        ]


class WaiverViewSet(viewsets.ModelViewSet):
    queryset = Waiver.objects.all()
    serializer_class = WaiverSerializer
    permission_classes = [WaiverDatePermission]
    renderer_classes = [JSONRenderer]
    lookup_field = "uuid"

    def retrieve(self, request, uuid):
        try:
            waiver = Waiver.objects.get(combatant__uuid=uuid)
            serializer = WaiverSerializer(waiver)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Waiver.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, uuid):
        """Update a combatant's waiver dates

        DRF can probably do this related object magic much more elegantly.
        TODO: Figure that out.

        We're also being a bit awful with HTTP verbs here. We're using PUT for everything
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            combatant = Combatant.objects.get(uuid=uuid)
        except Combatant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            waiver = Waiver.objects.get(combatant=combatant)
            waiver.date_signed = serializer.data.get("date_signed")
        except Waiver.DoesNotExist:
            waiver = Waiver(
                combatant=combatant, date_signed=serializer.data.get("date_signed")
            )
        finally:
            waiver.save()

        response_data = {
            "date_signed": waiver.date_signed,
            "expiration_date": waiver.expiration_date.strftime("%Y-%m-%d"),
        }
        return Response(response_data, status=status.HTTP_200_OK)
