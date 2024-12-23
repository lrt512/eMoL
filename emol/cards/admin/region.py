from django.contrib import admin
from cards.models.region import Region


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "country", "postal_format", "active")
    list_filter = ("country", "active")
    search_fields = ("code", "name")
