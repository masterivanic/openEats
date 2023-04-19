from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include
from django.urls import path
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularRedocView
from drf_spectacular.views import SpectacularSwaggerView

urlpatterns = [
    path("api/swagger/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("", lambda r: redirect("api/swagger-ui/")),
    path("admin/", admin.site.urls),
    path("", include("recipe.urls")),
    path("api/ingredient", include("ingredient.urls")),
    path("api/tag", include("tag.urls")),
]
