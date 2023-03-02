# -*- coding: utf-8 -*-
from django.contrib import admin

from cards.models.reminder_email import ReminderEmail

__all__ = ["ReminderEmailAdmin"]


@admin.register(ReminderEmail)
class ReminderEmailAdmin(admin.ModelAdmin):
    """Django Admin for ReminderEmail model"""

    pass
