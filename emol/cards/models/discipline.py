# -*- coding: utf-8 -*-
"""Model for a discipline"""

from django.db import models
from django.utils.text import slugify

__all__ = ["Discipline"]


class Discipline(models.Model):
    """Model a discipline.

    This class is an identifier and carrier for authorizations, marshals, and
    optionally card and waiver dates.

    See Card model docs for description

    Attributes:
        id: Primary key in the database
        name: Readable name for the discipline
        slug: A tokenized version of the name friendly to database and URL

    Relationships:
        authorizations: The set of Authorization records for this discipline
        marshals: The set of Marshal records for this discipline

    """

    name = models.CharField(max_length=255, null=False)
    slug = models.SlugField(max_length=255, unique=True, editable=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Discipline: {self.slug}>"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @classmethod
    def find(cls, discipline):
        """Look up a discipline.

        Args:
            discipline: A discipline slug (string) or id (int) or
                Discipline object

        Returns:
            Discipline object

        Raises:
            Discipline.DoesNotExist

        """
        if discipline is None:
            return None

        if isinstance(discipline, Discipline):
            return discipline

        if isinstance(discipline, str):
            try:
                return Discipline.objects.get(slug=discipline)
            except Discipline.DoesNotExist:
                pass

            return Discipline.objects.get(name=discipline)

        if isinstance(discipline, int):
            return Discipline.objects.get(id=discipline)

        raise ValueError("Invalid discipline type")
