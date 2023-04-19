from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Recipe
from .serializers import RecipeDetailsSerializer
from .serializers import RecipeSerializer
from .serializers import UserSerializer
from ingredient.models import Ingredient
from tag.models import Tag


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """define user api endpoint"""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class RecipeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):

    """define recipe api endpoint"""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_serializer_class(self):
        if self.action == "search" or self.action == "list":
            return RecipeDetailsSerializer
        return self.serializer_class

    def list(self, request):
        """override list method to apply new serializer"""

        queryset = Recipe.objects.all()
        serializer = RecipeDetailsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["GET"],
        detail=False,
        url_path=r"search/(?P<id_ing>[\d-]+)/(?P<id_tag>[\d-]+)",
    )
    def search(self, request, id_ing, id_tag):
        """search a recipe by ingredient and tag"""

        ingredients = get_object_or_404(Ingredient, pk=id_ing)
        tags = get_object_or_404(Tag, pk=id_tag)
        if ingredients.recipe.pk == tags.recipe.pk:
            data = Recipe.objects.get(pk=tags.recipe.pk)
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "not exist"}, status=status.HTTP_404_NOT_FOUND)
