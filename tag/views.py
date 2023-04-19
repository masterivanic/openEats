from rest_framework import mixins
from rest_framework import viewsets

from .models import Tag
from .serializers import TagSerializer


class TagViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
