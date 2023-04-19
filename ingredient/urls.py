from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet

router = DefaultRouter()

router.register("", IngredientViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
