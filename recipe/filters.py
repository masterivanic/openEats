import django_filters
from django.db import models
from django_filters import rest_framework as filters

from .models import Ingredient
from .models import Recipe


class RecipeFilter(filters.FilterSet):
    """recipe filter setup"""

    ingredient_name = filters.CharFilter(
        field_name="ingredient__name", lookup_expr="icontains"
    )
    tag_name = filters.CharFilter(field_name="tag__name", lookup_expr="icontains")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Recipe
        fields = ["name", "ingredient_name", "tag_name"]
        #     "name": ['exact'],
        #     "ingredient_name": ['exact'],
        #     "tag_name":['contains'],
        # }

        # filter_overrides = {
        #     models.CharField: {
        #         'filter_class': django_filters.CharFilter,
        #         'extra': lambda f: {
        #             'lookup_expr': 'icontains',
        #         },
        #     },
        # }

        # @property
        # def qs(self):
        #     parent = super().qs
        #     ingredient = Ingredient.objects.filter(pk__lte=100).get()
        #     return parent.filter(ingredient__pk=ingredient.pk)
