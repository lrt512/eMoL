# -*- coding: utf-8 -*-
from django.contrib import admin

from cards.models.privacy_acceptance import PrivacyAcceptance

__all__ = ["PrivacyAcceptanceAdmin"]


@admin.register(PrivacyAcceptance)
class PrivacyAcceptanceAdmin(admin.ModelAdmin):
    """Django Admin for PrivacyAcceptance model"""

    pass
