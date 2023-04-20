from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from recipe.models import Tag
from recipe.serializers import TagSerializer


class TagTestAPI(APITestCase):
    def test_listening_tags(self):
        response = self.client.get(reverse("tag-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tags_creation(self):
        tag_to_create = dict(name="string", description="string", recipe=0)

        response = self.client.post(reverse("tag-list"), tag_to_create)
        tag = Tag.objects.last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(tag.name, tag_to_create["name"])

    def test_tags_updating(self):
        tag = Tag.objects.all()[0:1]
        tag.name = "name"
        tag_serializer = TagSerializer(data=tag)
        if tag_serializer.is_valid():
            response = self.client.put(reverse("tag-list"), data=tag_serializer.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
