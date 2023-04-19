from django.db import models


class MainModel(models.Model):
    """parent models"""

    name = models.CharField(max_length=120, null=False, blank=True)
    description = models.CharField(max_length=120, null=False, blank=True)

    class Meta:
        abstract = True
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
