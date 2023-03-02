from django import template

from cards.models.user_permission import UserPermission
from current_user import get_current_user

register = template.Library()


@register.simple_tag
def has_global_permission(permission_slug, discipline_slug=None):
    user = get_current_user()
    return UserPermission.user_has_permission(user, permission_slug, discipline_slug)
