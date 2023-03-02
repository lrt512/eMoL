"""Proxy UserPermission checks as DRF permissions"""
from rest_framework import permissions

from cards.models.user_permission import UserPermission


class CombatantInfoPermission(permissions.BasePermission):
    """Check if user can read or write combatant info"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return UserPermission.user_has_permission(
                request.user, CombatantInfoPermission.READ_PERMISSION
            )

        return UserPermission.user_has_permission(
            request.user, CombatantInfoPermission.WRITE_PERMISSION
        )

    READ_PERMISSION = "read_combatant_info"
    WRITE_PERMISSION = "write_combatant_info"


class WaiverDatePermission(permissions.BasePermission):
    """Check if user can read or write waiver date"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return UserPermission.user_has_permission(
                request.user, WaiverDatePermission.READ_PERMISSION
            )

        return UserPermission.user_has_permission(
            request.user, WaiverDatePermission.WRITE_PERMISSION
        )

    READ_PERMISSION = "read_waiver_date"
    WRITE_PERMISSION = "write_waiver_date"


class CardDatePermission(permissions.BasePermission):
    """Check if user can write card date"""

    def has_object_permission(self, request, view, obj):
        if request.method == "PUT":
            return UserPermission.user_has_permission(
                request.user, CardDatePermission.WRITE_PERMISSION
            )

        return False

    WRITE_PERMISSION = "write_card_date"
