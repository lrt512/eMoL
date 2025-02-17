from cards.models.region import Region
from django.contrib import admin


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "country", "postal_format", "active")
    list_filter = ("country", "active")
    search_fields = ("code", "name")
