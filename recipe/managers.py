from django.db import models


class IngredientManager(models.Manager):
    pass


class RecipeManager(models.Manager):
    """recipe query manager, this filter is apply on backstage too"""

    def get_queryset(self):
        return super().get_queryset().filter(user__username="admin")
