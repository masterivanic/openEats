from django.contrib.auth.models import User
from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.db.models.functions import Upper


class Ingredient(models.Model):
    """This class define a ingredient of a recette"""

    name = models.CharField(max_length=120)
    description = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "ingredient"
        # constraints = [
        #     UniqueConstraint(Upper("name"), name="unique_ingredient_upper_name")
        # ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    """This class define a tag of a recette"""

    name = models.CharField(max_length=120)
    description = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "tag"
        ordering = ["name"]
        # constraints = [
        #     UniqueConstraint(Upper("name"), name="unique_tag_upper_name")
        # ]


class Recipe(models.Model):
    """This class define a user recette to cook"""

    name = models.CharField(max_length=120)
    description = models.TextField()
    preparation_time = models.DateTimeField()
    cuisson_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_recipe")
    ingredients = models.ManyToManyField(Ingredient)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "recipe"

    def __str__(self):
        return "{name} ({ingr})".format(
            name=self.name,
            ingr=", ".join(ingredient.name for ingredient in self.ingredients.all()),
        )
