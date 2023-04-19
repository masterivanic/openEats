from rest_framework import mixins
from rest_framework import viewsets

from .models import Ingredient
from .serializers import IngredientSerializer


class IngredientViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
