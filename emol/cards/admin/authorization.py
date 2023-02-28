# -*- coding: utf-8 -*-
from cards.models.authorization import Authorization
from django.contrib import admin

__all__ = ["AuthorizationAdmin"]


@admin.register(Authorization)
class AuthorizationAdmin(admin.ModelAdmin):
    """Django Admin for Authorization model"""

    readonly_fields = ["slug"]
