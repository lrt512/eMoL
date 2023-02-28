from django.db import models
from sso_user.models import SSOUser

from .discipline import Discipline
from .permission import Permission


class UserPermission(models.Model):
    user = models.ForeignKey(
        SSOUser, on_delete=models.CASCADE, related_name="user_permissions"
    )
    permission = models.ForeignKey(
        Permission, on_delete=models.CASCADE, related_name="user_permissionas"
    )
    discipline = models.ForeignKey(
        Discipline, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        unique_together = ("user", "permission", "discipline")

    def __str__(self):
        if self.discipline:
            return f"<UserPermission: {self.user.email} - {self.permission.name} ({self.discipline.name})"
        else:
            return (
                f"<UserPermission: {self.user.email} - {self.permission.name} (global)"
            )

    @classmethod
    def user_has_permission(cls, user, permission, related=None):
        """Check if the given user has a permission

        Args:
            user: The user to check
            permission: The permission to check
            related: Related object for non-global permissions
        """
        if user.is_anonymous:
            return False

        if user.is_superuser:
            return True

        permission_obj = Permission.find(permission)
        if hasattr(related, "discipline"):
            discipline_obj = related.getattr("discipline")
        else:
            discipline_obj = Discipline.find(related)

        return cls.objects.filter(
            user=user, permission=permission_obj, discipline=discipline_obj
        ).exists()
