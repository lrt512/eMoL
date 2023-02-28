# -*- coding: utf-8 -*-
from cards.models.reminder_email import ReminderEmail
from django.contrib import admin

__all__ = ["ReminderEmailAdmin"]


@admin.register(ReminderEmail)
class ReminderEmailAdmin(admin.ModelAdmin):
    """Django Admin for ReminderEmail model"""

    pass
