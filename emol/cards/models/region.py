from django.db import models


class Region(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_format = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
