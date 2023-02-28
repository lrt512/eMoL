# -*- coding: utf-8 -*-
"""Model for an authorization."""

from django.db import models
from django.utils.text import slugify

from .discipline import Discipline

__all__ = ["Authorization"]


class Authorization(models.Model):
    """Model an authorization for a discipline.

    Authorizations are referenced by the Card model through the
    CombatantAuthorization association model. See Card model docs for detail.

    Attributes:
        id: Primary key in the database
        slug: Slugified name for the authorization
        name: Full name of the authorization
        discipline: FK to the discipline this card is for
        is_primary: Authorization can be a primary authorization

    """

    slug = models.CharField(null=False, max_length=255)
    name = models.CharField(null=False, max_length=255)
    is_primary = models.BooleanField(null=False, default=False)
    discipline = models.ForeignKey(
        Discipline, on_delete=models.CASCADE, related_name="authorizations"
    )

    def __str__(self):
        return f"<Authorization: {self.discipline.slug}.{self.slug}>"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @classmethod
    def find(cls, discipline, authorization):
        """Look up an authorization.

        Args:
            discipline: A discipline slug (string) or id (int) or
                Discipline object
            authorization: An authorization slug (string) or id (int)
                or Authorization object

        Returns:
            Authorization object

        Raises:
            Authorization.DoesNotExist
             Discipline.DoesNotExist

        """
        #  Null case
        if isinstance(authorization, Authorization):
            return authorization

        discipline = Discipline.find(discipline)

        if isinstance(authorization, str):
            try:
                return (
                    Authorization.objects.filter(discipline=discipline)
                    .filter(slug=authorization)
                    .get()
                )
            except Authorization.DoesNotExist:
                pass

            # Let the DoesNotExist fly if not found here
            return (
                Authorization.objects.filter(discipline=discipline)
                .filter(name=authorization)
                .get()
            )
