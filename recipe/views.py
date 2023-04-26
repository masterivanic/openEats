import django_filters.rest_framework
from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.db.models import Q
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
        if self.action in ("list", "retrieve"):
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

        query_params = self.request.query_params.dict()
        serializer_search = SearchSerializer(data=query_params)
        serializer_search.is_valid(raise_exception=True)

        ingredient_name = serializer_search.validated_data.get("ingredient_name")
        tag_name = serializer_search.validated_data.get("tag_name")
        name = serializer_search.validated_data.get("name")

        if all([ingredient_name, tag_name, name]):
            # here we make query too according to case sensitive
            queryset = Recipe.objects.filter(
                Q(ingredient__name__iexact=ingredient_name),
                Q(tag__name__iexact=tag_name),
                Q(name__iexact=name),
            )

            page = self.paginate_queryset(queryset)
            if page:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(status.HTTP_204_NO_CONTENT)


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
