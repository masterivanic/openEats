from django.contrib.auth.models import User
from django.db import models

from .managers import RecipeManager


class Ingredient(models.Model):
    """This class define a ingredient of a recette"""

    name = models.CharField(max_length=120, null=False, blank=True)
    description = models.CharField(max_length=120, null=False, blank=True)

    class Meta:
        db_table_comment = "Ingredient table"
        verbose_name = "Ingredient"

    def __str__(self):
        return self.name


class Tag(models.Model):
    """This class define a tag of a recette"""

    name = models.CharField(max_length=120, null=False, blank=True)
    description = models.CharField(max_length=120, null=False, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table_comment = "Tag table"
        verbose_name = "Tag"
        ordering = ["name"]


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
    ingredient = models.ManyToManyField(Ingredient)
    tag = models.ManyToManyField(Tag, blank=True)

    class Meta:
        ordering = ["name"]
        db_table_comment = "Recipe table"
        verbose_name = "Recipe"

    def __str__(self):
        return "%s (%s)" % (
            self.name,
            ", ".join(ingredient.name for ingredient in self.ingredient.all()),
        )
