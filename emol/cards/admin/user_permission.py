# -*- coding: utf-8 -*-
from cards.models.user_permission import UserPermission
from django.contrib import admin


@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    """Django Admin for UserPermission model"""

    pass
