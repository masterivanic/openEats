from typing import List

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from recipe.models import Ingredient
from recipe.models import Recipe
from recipe.models import Tag
from recipe.serializers import RecipeSerializer
from recipe.serializers import UserSerializer


@pytest.fixture
def create_ingredient(db) -> Ingredient:
    """create ingredient in test db"""
    return Ingredient.objects.create(name="Mayonnaise", description="très degoutant")


@pytest.fixture
def create_tag(db) -> Tag:
    return Tag.objects.create(name="Recette italienne", description="trop bon")


@pytest.fixture
def create_user(db) -> User:
    return User.objects.create(username="tom", email="tom@yahoo.fr", password="anypass")


@pytest.fixture
def ingredient_list(db) -> list:
    return []


@pytest.fixture
def tag_list(db) -> list:
    return []


@pytest.fixture(autouse=True)
def append_tag(tag_list, create_tag):
    return tag_list.append(create_tag)


@pytest.fixture(autouse=True)
def append_ingredient(ingredient_list, create_ingredient):
    return ingredient_list.append(create_ingredient)


@pytest.fixture
def create_recipe(db, create_user, ingredient_list, tag_list) -> Recipe:
    recipe = Recipe.objects.create(
        name="test",
        description="test",
        preparation_time="2023-04-19T10:51:01.889Z",
        cuisson_time="2023-04-19T10:51:01.889Z",
        user=create_user,
    )
    recipe.ingredient.set(ingredient_list)
    recipe.tag.set(tag_list)
    return recipe


@pytest.fixture
def create_recipe_list(db, create_recipe) -> List[Recipe]:
    recipe_list: List[Recipe] = []
    recipe_list.append(create_recipe)
    return recipe_list


@pytest.fixture
def create_user_list(db) -> List[User]:
    user_list: List[User] = []
    user_list.append(User.objects.create(username="royd"))
    user_list.append(User.objects.create(username="kartin"))
    return user_list


def test_user_listing(create_user_list) -> None:
    response = APIClient().get(reverse("user-list"))
    assert response.status_code == status.HTTP_200_OK
    assert len(create_user_list) == 2


def test_user_creation(create_user) -> None:
    user_to_create = dict(username="Jean", email="jean@gmail.com", password="anypass")
    serializer = UserSerializer(user_to_create)
    response = APIClient().post(reverse("user-list"), serializer.data)
    assert response.status_code == status.HTTP_201_CREATED


def test_user_update(create_user) -> None:
    create_user.username = "Olivier"
    create_user.save()
    user_id = create_user.pk
    serializer = UserSerializer(create_user)
    response = APIClient().put(reverse("user-detail", args=[user_id]), serializer.data)
    user_from_db = User.objects.get(username="Olivier")
    assert response.status_code == status.HTTP_200_OK
    assert user_from_db.username == "Olivier"


def test_recipe_listing(create_recipe_list) -> None:
    response = APIClient().get(reverse("recipe-list"))
    assert response.status_code == status.HTTP_200_OK
    assert len(create_recipe_list) == 1


def test_recipe_creation(create_user, ingredient_list, tag_list) -> None:
    recipe_to_create = dict(
        name="Sushi au macaron",
        description="meilleur plat japonais",
        preparation_time="2023-04-19T10:51:01.889Z",
        cuisson_time="2023-04-19T10:51:01.889Z",
        user=create_user,
        ingredient=ingredient_list,
        tag=tag_list,
    )

    serializer = RecipeSerializer(recipe_to_create)
    response = APIClient().post(reverse("recipe-list"), serializer.data)
    assert response.status_code == status.HTTP_201_CREATED


def test_recipe_update(create_recipe) -> None:
    create_recipe.name = "autre recette"
    create_recipe.save()
    recipe_id = create_recipe.pk
    serializer = RecipeSerializer(create_recipe)
    response = APIClient().put(
        reverse("recipe-detail", args=[recipe_id]), serializer.data
    )
    recipe_from_db = Recipe.objects.get(name="autre recette")
    assert response.status_code == status.HTTP_200_OK
    assert recipe_from_db.name == "autre recette"
