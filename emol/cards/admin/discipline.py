# -*- coding: utf-8 -*-
from cards.models.discipline import Discipline
from django.contrib import admin


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    """Django Admin for Discipline model"""

    readonly_fields = ["slug"]
