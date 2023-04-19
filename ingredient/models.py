from django.db import models

from openeats.main_models import MainModel
from recipe.models import Recipe


class Ingredient(MainModel):
    """This class define a ingredient of a recette"""

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name="the related recipe", null=True
    )

    class Meta(MainModel.Meta):
        db_table_comment = "Ingredient table"
        verbose_name = "Ingredient"
