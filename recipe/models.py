from django.contrib.auth.models import User
from django.db import models


class Recipe(models.Model):
    """This class define a user recette to cook"""

    name = models.CharField(max_length=120, null=False, blank=True)
    description = models.TextField()
    preparation_time = models.DateTimeField()
    cuisson_time = models.DateTimeField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ["name"]
        db_table_comment = "Recipe table"
        verbose_name = "Recipe"

    def __str__(self):
        return self.name
