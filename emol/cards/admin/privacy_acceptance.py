# -*- coding: utf-8 -*-
from cards.models.privacy_acceptance import PrivacyAcceptance
from django.contrib import admin

__all__ = ["PrivacyAcceptanceAdmin"]


@admin.register(PrivacyAcceptance)
class PrivacyAcceptanceAdmin(admin.ModelAdmin):
    """Django Admin for PrivacyAcceptance model"""

    pass
