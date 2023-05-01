from typing import List

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from recipe.models import Ingredient
from recipe.serializers import IngredientSerializer


@pytest.fixture
def create_ingredient(db) -> Ingredient:
    """create ingredient in test db"""
    return Ingredient.objects.create(name="Mayonnaise", description="très degoutant")


@pytest.fixture
def create_ingredients_list(db) -> List[Ingredient]:
    ingredient_list: List[Ingredient] = []
    ingredient_list.append(
        Ingredient.objects.create(name="Mayonnaise", description="très degoutant")
    )
    ingredient_list.append(
        Ingredient.objects.create(name="Poivre", description="parfait")
    )
    ingredient_list.append(
        Ingredient.objects.create(name="Oignon", description="parfait")
    )
    return ingredient_list


def test_ingredient_listing(create_ingredients_list) -> None:
    response = APIClient().get(reverse("ingredient-list"))
    assert response.status_code == status.HTTP_200_OK
    assert len(create_ingredients_list) == 3


def test_ingredient_update(create_ingredient) -> None:
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


def test_ingredient_creation(create_ingredient) -> None:
    ingredient_to_create = dict(name="Aubergine", description="trop bon")
    seriliazer = IngredientSerializer(ingredient_to_create)
    response = APIClient().post(reverse("ingredient-list"), seriliazer.data)
    assert response.status_code == status.HTTP_201_CREATED
