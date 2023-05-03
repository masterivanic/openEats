from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from recipe.models import Ingredient
from recipe.serializers import IngredientSerializer


class IngredientTestAPI:
    def test_ingredient_listing(self, create_ingredients_list) -> None:
        response = APIClient().get(reverse("ingredient-list"))
        assert response.status_code == status.HTTP_200_OK
        assert len(create_ingredients_list) == 3

    def test_ingredient_update(self, create_ingredient) -> None:
        create_ingredient.name = "Piment"
        create_ingredient.save()
        ing_id = create_ingredient.pk
        serializer = IngredientSerializer(create_ingredient)
        response = APIClient().put(
            reverse("ingredient-detail", args=[ing_id]), serializer.data
        )
        ing_from_db = Ingredient.objects.get(name="Piment")
        assert response.status_code == status.HTTP_200_OK
        assert ing_from_db.name == "Piment"

    def test_ingredient_creation(self, create_ingredient) -> None:
        ingredient_to_create = dict(name="Aubergine", description="trop bon")
        seriliazer = IngredientSerializer(ingredient_to_create)
        response = APIClient().post(reverse("ingredient-list"), seriliazer.data)

        ing_from_db = Ingredient.objects.get(name="Aubergine")
        serializer_create = IngredientSerializer(create_ingredient)

        assert response.status_code == status.HTTP_201_CREATED
        assert ing_from_db.name == "Aubergine"
        assert not (response.data == serializer_create.data)
