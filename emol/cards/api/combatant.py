import logging

from cards.models.combatant import Combatant
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .permissions import CombatantInfoPermission

logger = logging.getLogger(__name__)


class CombatantListSerializer(ModelSerializer):
    class Meta:
        model = Combatant
        fields = [
            "legal_name",
            "sca_name",
            "card_id",
            "uuid",
            "accepted_privacy_policy",
        ]


class CombatantListViewSet(ReadOnlyModelViewSet):
    """
    API endpoint for the combatant list view
    """

    queryset = Combatant.objects.all()
    serializer_class = CombatantListSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = [CombatantInfoPermission]


class CombatantSerializer(ModelSerializer):
    class Meta:
        model = Combatant
        fields = [
            "uuid",
            "email",
            "sca_name",
            "legal_name",
            "phone",
            "address1",
            "address2",
            "city",
            "province",
            "postal_code",
            "dob",
            "member_expiry",
            "member_number",
        ]

        optional_fields = [
            "uuid",
            "member_expiry",
            "member_number",
        ]

        clean_blank_strings = [
            "sca_name",
            "member_expiry",
            "member_number",
            "address2",
            "dob",
            "uuid",
        ]

    member_expiry = serializers.DateField(format="%Y-%m-%d", allow_null=True)

    def to_internal_value(self, data):
        """
        Hacky way to get at the data to clean it before DRF's validators
        go insane.
        """
        # Clean up blank strings on specified fields
        for attr in __class__.Meta.clean_blank_strings:
            if attr in data and len(data[attr]) == 0:
                data[attr] = None

        return super().to_internal_value(data)


class CombatantViewSet(ModelViewSet):
    """
    API endpoint that allows combatants to be viewed or edited.
    """

    queryset = Combatant.objects.all()
    serializer_class = CombatantSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = [CombatantInfoPermission]
    lookup_field = "uuid"
