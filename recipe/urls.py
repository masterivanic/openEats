from django.urls import include
from django.urls import path
from django.urls import re_path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet
from .views import RecipeViewSet
from .views import TagViewSet
from .views import UserViewSet

router = DefaultRouter()

router.register("api/v1/user", UserViewSet)
router.register("api/v1/recipe", RecipeViewSet, basename="recipe")
router.register("api/v1/ingredient", IngredientViewSet, basename="ingredient")
router.register("api/v1/tag", TagViewSet, basename="tag")


urlpatterns = [
    path("", include(router.urls)),
]
