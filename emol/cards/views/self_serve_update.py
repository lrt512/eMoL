import logging

from cards.models import Combatant, Region, UpdateCode
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

logger = logging.getLogger("cards")


class SelfServeUpdateSerializer(ModelSerializer):
    """Like a CombatantSerializer, but can't update email address"""

    class Meta:
        model = Combatant
        fields = [
            "sca_name",
            "legal_name",
            "phone",
            "address1",
            "address2",
            "city",
            "province",
            "postal_code",
            "member_expiry",
            "member_number",
        ]

        extra_kwargs = {
            "member_expiry": {
                "format": "%Y-%m-%d",
                "allow_null": True,
                "required": False,
            },
            "member_number": {"required": False},
            "address2": {"required": False},
            "sca_name": {"required": False},
            "legal_name": {"required": True},
            "phone": {"required": True},
            "address1": {"required": True},
            "city": {"required": True},
            "province": {"required": True},
            "postal_code": {"required": True},
        }

    # Fields that should be cleaned up if they are blank strings
    clean_fields = [
        "sca_name",
        "member_expiry",
        "member_number",
        "address2",
    ]

    def validate(self, data):
        """
        Ensure that if member_expiry is specified, then member_number is also specified.
        """
        if data.get("member_expiry") and not data.get("member_number"):
            raise serializers.ValidationError(
                {
                    "member_number": "Member number is required when specifying an expiry date."
                }
            )
        return data

    def to_internal_value(self, data):
        """
        Clean up blank strings for specified fields before validation
        """
        data = super().to_internal_value(data)
        for attr in self.clean_fields:
            if attr in data and not data[attr]:
                data[attr] = None

        return data


def serializer_errors_to_strings(serializer):
    """Convert serializer errors to strings for display"""
    errors = serializer.errors
    error_messages = []
    for field, error_list in errors.items():
        for error_detail in error_list:
            error_messages.append(f"{field}: {error_detail}")

    return error_messages


@csrf_protect
@require_http_methods(["GET", "POST"])
def self_serve_update(request, code):
    """Handle self-serve updates"""
    try:
        update_code = UpdateCode.objects.get(code=code)
        context = {
            "self_serve": True,
            "code": code,
            "combatant": update_code.combatant,
            "regions": Region.objects.all(),
        }

        if request.method == "GET":
            return render(request, "combatant/self_serve_update.html", context)

        serializer = SelfServeUpdateSerializer(
            instance=update_code.combatant, data=request.POST, partial=True
        )

        if not serializer.is_valid():
            context["message"] = "There was an error updating your information."
            context["errors"] = serializer_errors_to_strings(serializer)
            logger.error(
                "Self-serve update failed for code %s with errors: %s",
                code,
                serializer.errors,
            )
            return render(request, "combatant/self_serve_update.html", context)

        serializer.save()
        logger.info(
            "Successfully updated combatant information for code %s, combatant_id: %s",
            code,
            update_code.combatant.id,
        )
        update_code.delete()
        return render(
            request,
            "message/message.html",
            {"message": "Your information has been updated successfully."},
        )
    except UpdateCode.DoesNotExist:
        return render(
            request,
            "message/message.html",
            {
                "message": "The update code provided is invalid or has already been used."
            },
        )
    except Exception as e:
        logger.exception("Unexpected error in self_serve_update for code %s", code)
        return render(
            request,
            "message/message.html",
            {"message": "An unexpected error occurred. Please try again later."},
        )
