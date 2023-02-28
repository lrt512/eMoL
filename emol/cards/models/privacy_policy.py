from django.db import models


class PrivacyPolicy(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Privacy policy version {self.version} ({self.created_at})"

    @classmethod
    def latest_version(cls):
        return cls.objects.latest("created_at")

    @property
    def latest_text(self):
        return self.latest_verson.text
