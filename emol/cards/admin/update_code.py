# -*- coding: utf-8 -*-
from cards.models import UpdateCode
from django.contrib import admin

__all__ = ["UpdateCodeAdmin"]


@admin.register(UpdateCode)
class UpdateCodeAdmin(admin.ModelAdmin):
    """Django Admin for UpdateCode model"""

    readonly_fields = ["combatant", "code", "expires_at"]
