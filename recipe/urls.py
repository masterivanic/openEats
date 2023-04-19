from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import RecipeViewSet
from .views import UserViewSet

router = DefaultRouter()

router.register("api/user", UserViewSet)
router.register("api/recipe", RecipeViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
