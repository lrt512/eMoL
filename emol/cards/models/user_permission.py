import logging

from django.db import models

from sso_user.models import SSOUser

from .discipline import Discipline
from .permission import Permission

logger = logging.getLogger("cards")


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
    def user_has_permission(cls, user, permission, discipline=None):
        """Check if the given user has a permission

        Args:
            user: The user to check
            permission: The permission to check
            related: Related object for non-global permissions
        """
        if user.is_anonymous:
            return False

        # if user.is_superuser:
        #    return True

        try:
            permission = Permission.find(permission)
        except Permission.DoesNotExist:
            logger.error(f"Permission {permission} does not exist")
            return False

        logger.debug(f"Permission: %s for %s", permission, user)
        if permission.is_global:
            permit = cls.objects.filter(user=user, permission=permission).exists()
            logger.debug("Is global permission")
            logger.debug("Permission result: %s", permit)
            return permit

        logger.debug("Is discipline permission")
        try:
            permit = cls.objects.filter(
                user=user, permission=permission, discipline=discipline
            ).exists()
        except cls.DoesNotExist:
            permit = False
        except Exception as e:
            logger.exception(
                f"Error while checking permission {permission.name} for user {user.email}: {str(e)}"
            )
            permit = False

        logger.debug("Permission result: %s", permit)
        return permit
