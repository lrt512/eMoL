import logging

from cards.mail import send_privacy_policy
from cards.models.combatant import Combatant
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView


class ResendPrivacySerializer(serializers.Serializer):
    combatant_uuid = serializers.UUIDField()


logger = logging.getLogger(__name__)


class ResendPrivacyView(APIView):
    def post(self, request):
        """Resend the privacy policy email to a combatant"""

        serializer = ResendPrivacySerializer(data=request.data)

        if serializer.is_valid():
            combatant_uuid = serializer.validated_data.get("combatant_uuid")
            try:
                combatant = Combatant.objects.get(uuid=combatant_uuid)
                if combatant.accepted_privacy_policy is False:
                    send_privacy_policy(combatant)
                    return Response(
                        {
                            "message": f"Sent privacy policy reminder to {combatant.name}"
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    logger.warn(
                        f"Combatant {combatant} already accepted the privacy policy"
                    )
                    return Response(
                        {
                            "message": f"{combatant.name} already accepted the privacy policy"
                        },
                        status=status.HTTP_208_ALREADY_REPORTED,
                    )
            except Combatant.DoesNotExist:
                return Response(
                    {"message": f"No combatant for ID {combatant_uuid}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
