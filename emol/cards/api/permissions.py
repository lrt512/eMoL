"""Proxy UserPermission checks as DRF permissions"""
from cards.models.user_permission import UserPermission
from rest_framework import permissions


class CombatantInfoPermission(permissions.BasePermission):
    """Check if user can read or write combatant info"""

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return UserPermission.user_has_permission(
                request.user, "read_combatant_info"
            )

        if request.method in ("POST", "PATCH", "DELETE"):
            return UserPermission.user_has_permission(
                request.user, "read_combatant_info"
            )

        return False


class WaiverDatePermission(permissions.BasePermission):
    """Check if user can read or write waiver date"""

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return UserPermission.user_has_permission(request.user, "read_waiver_date")

        if request.method in ("POST", "PATCH"):
            return UserPermission.user_has_permission(request.user, "write_waiver_date")

        return False


class CardDatePermission(permissions.BasePermission):
    """Check if user can write card date"""

    def has_object_permission(self, request, view, obj):
        if request.method in ("PUT"):
            return UserPermission.user_has_permission(
                request.user, "write_card_date"
            )

        return False
