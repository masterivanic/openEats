from django.contrib.auth.models import User
from django.db.models import Prefetch
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Ingredient
from .models import Recipe
from .models import Tag
from .serializers import IngredientSerializer
from .serializers import RecipeDetailsSerializer
from .serializers import RecipeSerializer
from .serializers import TagSerializer
from .serializers import UserSerializer


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """define user api endpoint"""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):

    """define recipe api endpoint"""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ("list"):
            return RecipeDetailsSerializer
        return self.serializer_class

    def list(self, request):
        """override list method to apply new serializer"""

        queryset = Recipe.objects.prefetch_related(
            Prefetch("ingredient"), Prefetch("tag")
        )
        results = []
        for q in queryset:
            obj = {
                "name": q.name,
                "description": q.description,
                "preparation_time": q.preparation_time,
                "cuisson_time": q.cuisson_time,
                "user": q.user.pk,
                "user": 0,
                "ingredients": [ing for ing in q.ingredient.all().values()],
                "tags": [tag for tag in q.tag.all().values()],
            }
            results.append(obj)
        return Response(results, status=status.HTTP_200_OK)

    @action(
        methods=["GET"],
        detail=False,
        url_path=r"search/(?P<ingredient_name>\w+)/(?P<tag_name>\w+)/(?P<recipe_name>\w+)",
    )
    def search(
        self,
        request,
        ingredient_name: str = None,
        tag_name: str = None,
        recipe_name: str = None,
    ) -> Response:
        """
        search a recipe by ingredient and tag

        :request: the request object
        :param nom_ingredient: ingredient name
        :param nom_tag: tags name
        :param recipe_name: recipe name
        :return: an Http response
        """

        if ingredient_name:
            queryset = Recipe.objects.prefetch_related(Prefetch("ingredient"))
            list_recette = [
                (recette, recette.ingredient.filter(name=ingredient_name))
                for recette in queryset
            ]
            queryset = [recette[0] for recette in list_recette]
        elif tag_name:
            queryset = Recipe.objects.prefetch_related(Prefetch("tag"))
            list_tags = [
                (recette, recette.tag.filter(name=tag_name)) for recette in queryset
            ]
            queryset = [recette[0] for recette in list_tags]

        elif recipe_name:
            queryset = Recipe.objects.filter(name=recipe_name)

            serializer = self.get_serializer(data=queryset)
            if serializer.is_valid():
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "not exist"}, status=status.HTTP_404_NOT_FOUND)


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = [AllowAny]


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [AllowAny]
