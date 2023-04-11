# -*- coding: utf-8 -*-
from django.contrib import admin

from cards.models.reminder import Reminder

__all__ = ["ReminderAdmin"]


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    """Django Admin for ReminderEmail model"""

    pass
