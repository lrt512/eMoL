# -*- coding: utf-8 -*-
"""Model for a discipline"""

from django.db import models
from django.utils.text import slugify


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
        return f"<Discipline: {self.name}>"

    def save(self, *args, **kwargs):
        if not self.pk:
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
            ValueError: If discipline is None
            Discipline.DoesNotExist: If discipline is not found

        """
        if isinstance(discipline, Discipline):
            return discipline

        query = models.Q(slug=discipline) | models.Q(name=discipline)
        discipline = cls.objects.filter(query).first()
        if discipline is None:
            raise cls.DoesNotExist(f"No discipline found for {discipline}")

        return discipline
