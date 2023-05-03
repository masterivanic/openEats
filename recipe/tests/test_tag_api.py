import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from recipe.models import Tag
from recipe.serializers import TagSerializer


@pytest.mark.django_db
class TagTestAPI:
    def test_listening_tags(self, create_tag_list) -> None:
        response = APIClient().get(reverse("tag-list"))
        assert response.status_code == status.HTTP_200_OK
        assert len(create_tag_list) == 3

    def test_tags_creation(self, create_tag) -> None:
        tag_to_create = dict(name="tag4", description="")
        serializer = TagSerializer(tag_to_create)
        response = APIClient().post(reverse("tag-list"), serializer.data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_tags_update(self, create_tag) -> None:
        create_tag.name = "Recette cubaine"
        create_tag.save()
        tag_id = create_tag.pk
        serializer = TagSerializer(create_tag)
        response = APIClient().put(
            reverse("tag-detail", args=[tag_id]), serializer.data
        )
        tag_from_db = Tag.objects.get(name="Recette cubaine")
        assert response.status_code == status.HTTP_200_OK
        assert tag_from_db.name == "Recette cubaine"
