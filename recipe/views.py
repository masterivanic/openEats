import django_filters.rest_framework
from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.db.models import Q
from django.db.models import When
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from drf_spectacular.utils import OpenApiParameter
from rest_framework import filters
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from .filters import RecipeFilter
from .models import Ingredient
from .models import Recipe
from .models import Tag
from .serializers import IngredientSerializer
from .serializers import RecipeDetailsSerializer
from .serializers import RecipeSerializer
from .serializers import SearchSerializer
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


@extend_schema_view(
    search=extend_schema(
        description="API endpoint to search a recipe \n\n",
        parameters=[SearchSerializer],
    ),
)
class RecipeViewSet(viewsets.ModelViewSet):

    """define recipe api endpoint"""

    queryset = Recipe.objects.prefetch_related("ingredient", "tag")
    serializer_class = RecipeSerializer
    filterset_class = RecipeFilter
    filter_backends = [filters.SearchFilter]
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve", "search"):
            return RecipeDetailsSerializer
        return self.serializer_class

    @action(
        methods=["GET"],
        detail=False,
        url_path=r"search",
    )
    def search(
        self,
        request,
    ) -> Response:
        """
        search a recipe by ingredient and tag

        :request: the request object
        :param nom_ingredient: ingredient name
        :param nom_tag: tags name
        :param recipe_name: recipe name
        :return: an Http response
        """
        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset)
        serializer = RecipeDetailsSerializer(filtered_queryset, many=True)
        return Response(serializer.data)


class IngredientViewSet(viewsets.ModelViewSet):
    """define ingredient api endpoint"""

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = [AllowAny]


class TagViewSet(viewsets.ModelViewSet):
    """define tag api endpoint"""

    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [AllowAny]
