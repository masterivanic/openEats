from django.contrib.auth.models import User
from django.db import models

from openeats.main_models import MainModel


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


class Tag(MainModel):
    """This class define a tag of a recette"""

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name="the related recipe", null=True
    )

    class Meta(MainModel.Meta):
        db_table_comment = "Tag table"
        verbose_name = "Tag"


class Ingredient(MainModel):
    """This class define a ingredient of a recette"""

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name="the related recipe", null=True
    )

    class Meta(MainModel.Meta):
        db_table_comment = "Ingredient table"
        verbose_name = "Ingredient"
