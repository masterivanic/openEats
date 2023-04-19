from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ingredient.models import Ingredient
from ingredient.serializers import IngredientSerializer


class IngredientTestAPI(APITestCase):
    def test_ingredient_listing(self):
        response = self.client.get(reverse("ingredient:ingredient-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ingredient_creation(self):
        ingredient_to_create = dict(name="string", description="string", recipe=0)
        response = self.client.post(
            reverse("ingredient:ingredient-list"), ingredient_to_create
        )
        ingredient = Ingredient.objects.last()

        assert response.status_code == status.HTTP_201_CREATED
        assert ingredient.name == ingredient_to_create["name"]

    def test_ingredient_update(self):
        ingredient = Ingredient.objects.all()[0:1]
        ingredient.description = "description test"
        ingredient_serializer = IngredientSerializer(data=ingredient)
        response = self.client.put(
            reverse("ingredient:ingredient-list"), ingredient_serializer.data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
