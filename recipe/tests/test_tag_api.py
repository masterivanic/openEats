from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from recipe.models import Tag
from recipe.serializers import TagSerializer


class TagTestAPI(APITestCase):
    """Tag api endpoint test"""

    def test_listening_tags(self) -> None:
        response = self.client.get(reverse("tag-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tags_creation(self) -> None:
        tag_to_create = dict(name="string", description="string", recipe=0)
        response = self.client.post(reverse("tag-list"), tag_to_create)
        tag = Tag.objects.last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(tag.name, tag_to_create["name"])

    def test_tags_updating(self) -> None:
        tag = Tag.objects.all()[0:1]
        tag[0].name = "name"
        tag_serializer = TagSerializer(tag[0])
        if tag_serializer.is_valid():
            response = self.client.put(reverse("tag-list", args=[tag[0].pk]), data=tag_serializer.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
