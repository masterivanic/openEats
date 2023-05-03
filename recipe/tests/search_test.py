from typing import List

import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse
from django_query_capture.test_utils import AssertInefficientQuery
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from recipe.models import Ingredient
from recipe.models import Recipe
from recipe.models import Tag
from recipe.serializers import RecipeDetailsSerializer


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


def test_that_user_can_filter_recipe_using_name_recipe(create_recipe_list) -> None:
    params = {"name": "test"}
    with AssertInefficientQuery(num=19):
        factory = APIClient().get(reverse("recipe-search"), params)
        assert factory.status_code == status.HTTP_200_OK
        assert len(create_recipe_list) == 1


def test_that_user_can_filter_recipe_using_ingredient(create_recipe_list) -> None:
    params = {"ingredient_name": "farine"}
    recipe = Recipe.objects.filter(
        ingredient__name__icontains=params["ingredient_name"]
    )
    serializer = RecipeDetailsSerializer(recipe, many=True)
    response = APIClient().get(reverse("recipe-search"), params)
    assert response.status_code == status.HTTP_200_OK


def test_that_user_can_filter_recipe_using_tag(create_recipe_list) -> None:
    params = {"tag_name": "Halal"}
    recipe = Recipe.objects.filter(tag__name__icontains=params["tag_name"])
    serializer = RecipeDetailsSerializer(recipe, many=True)

    response = APIClient().get(reverse("recipe-search"), params)
    assert response.status_code == status.HTTP_200_OK


def test_that_user_can_filter_recipe_combining_two_filters(create_recipe_list) -> None:
    params = {"tag_name": "Halal", "ingredient_name": "Fa"}
    recipe = Recipe.objects.filter(
        Q(tag__name__icontains=params["tag_name"]),
        Q(ingredient__name__icontains=params["ingredient_name"]),
    )
    serializer = RecipeDetailsSerializer(recipe, many=True)
    response = APIClient().get(reverse("recipe-search"), params)
    assert response.status_code == status.HTTP_200_OK


def test_that_user_can_filter_recipe_combining_tree_filters(create_recipe_list) -> None:
    params = {"ingredient_name": "Fa", "name": "hello", "tag_name": "Fa"}
    recipe = Recipe.objects.filter(
        Q(tag__name__icontains=params["tag_name"]),
        Q(ingredient__name__icontains=params["ingredient_name"]),
        Q(name__icontains=params["name"]),
    )
    response = APIClient().get(reverse("recipe-search"), params)
    serializer = RecipeDetailsSerializer(recipe, many=True)

    assert response.status_code == status.HTTP_200_OK
    assert not (len(serializer.data) == len(create_recipe_list))


def test_that_search_dont_return_items_that_where_not_asked_through_filtering(
    create_recipe_list,
) -> None:
    params = {"name": "test"}
    recipe_dont_expected = Recipe.objects.filter(tag__name__icontains="vegan")
    serializer_recipe = RecipeDetailsSerializer(recipe_dont_expected, many=True)

    response = APIClient().get(reverse("recipe-search"), params)
    response.status_code == status.HTTP_200_OK
    assert not (serializer_recipe.data == response.data)
