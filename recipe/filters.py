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
