# -*- coding: utf-8 -*-
from cards.models.card import Card
from cards.models.combatant_authorization import CombatantAuthorization
from cards.models.combatant_warrant import CombatantWarrant
from django.contrib import admin

__all__ = ["CardAdmin"]


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    """Django Admin for Card model"""


@admin.register(CombatantAuthorization)
class CombatantAuthorizationAdmin(admin.ModelAdmin):
    """Django Admin for CombatantAuthorization model"""


@admin.register(CombatantWarrant)
class CombatantWarrantAdmin(admin.ModelAdmin):
    """Django Admin for CombatantWarrant model"""
