from django.db import models

from openeats.main_models import MainModel
from recipe.models import Recipe


class Tag(MainModel):
    """This class define a tag of a recette"""

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name="the related recipe", null=True
    )

    class Meta(MainModel.Meta):
        db_table_comment = "Tag table"
        verbose_name = "Tag"
