from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def settings_notice():
    if settings.SETTINGS_MODULE == 'emol.settings.dev_settings':
        return mark_safe('<span class="warning">Using default development settings</span>')
    
    return ''
