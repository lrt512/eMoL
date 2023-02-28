from django.db import models


class CombatantUpdate(models.Model):
    combatant = models.ForeignKey("Combatant", on_delete=models.CASCADE)
    code = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.combatant.email} - {self.code}"


class InvalidCode(Exception):
    pass
