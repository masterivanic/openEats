from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import TagViewSet

router = DefaultRouter()

app_name = "tag"
router.register("", TagViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
