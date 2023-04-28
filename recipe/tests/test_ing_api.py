from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.shortcuts import get_object_or_404

from recipe.models import Ingredient
from recipe.serializers import IngredientSerializer


class IngredientTestAPI(APITestCase):
    """Ingredient api endpoint test"""

    def test_ingredient_listing(self) -> None:
        response = self.client.get(reverse("ingredient-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ingredient_creation(self) -> None:
        ingredient_to_create = dict(name="string", description="string", recipe=1)

        response = self.client.post(reverse("ingredient-list"), ingredient_to_create)
        ingredient = Ingredient.objects.last()

        assert response.status_code == status.HTTP_201_CREATED
        assert ingredient.name == ingredient_to_create["name"]

    def test_ingredient_update(self) -> None:
        ingredient_data = {
            "name": "test update",
            "description": "description test"
        }

        response = self.client.put(
            reverse("ingredient-detail",  args=[1]),    
            ingredient_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
