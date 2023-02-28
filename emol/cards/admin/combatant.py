# -*- coding: utf-8 -*-
from cards.models.combatant import Combatant
from django.contrib import admin

__all__ = ["CombatantAdmin"]


@admin.register(Combatant)
class CombatantAdmin(admin.ModelAdmin):
    """Django Admin for Combatant model"""

    readonly_fields = ("uuid", "last_update")
