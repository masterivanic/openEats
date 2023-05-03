from typing import List

import pytest
from django.contrib.auth.models import User

from recipe.models import Ingredient
from recipe.models import Recipe
from recipe.models import Tag


@pytest.fixture(scope="session")
def create_ingredient(django_db_blocker) -> Ingredient:
    """create ingredient in test db"""
    with django_db_blocker.unblock():
        Ingredient.objects.create(name="Mayonnaise", description="très degoutant")


@pytest.fixture(scope="session")
def create_ingredients_list(django_db_blocker) -> List[Ingredient]:
    ingredient_list: List[Ingredient] = []
    with django_db_blocker.unblock():
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


@pytest.fixture()
def create_tag() -> Tag:
    return Tag.objects.create(name="Recette italienne", description="trop bon")


@pytest.fixture()
def create_tag_list() -> List[Tag]:
    tag_list: List[Tag] = []
    tag_list.append(Tag.objects.create(name="first", description=""))
    tag_list.append(Tag.objects.create(name="Second", description=""))
    tag_list.append(Tag.objects.create(name="Third", description=""))
    return tag_list


@pytest.fixture(scope="session")
def create_user(django_db_blocker) -> User:
    with django_db_blocker.unblock():
        User.objects.create(username="tom", email="tom@yahoo.fr", password="anypass")


@pytest.fixture(scope="session")
def ingredient_list(django_db_blocker) -> list:
    return []


@pytest.fixture(scope="session")
def tag_list(django_db_blocker) -> list:
    return []


@pytest.fixture(autouse=True, scope="session")
def append_tag(tag_list, create_tag):
    return tag_list.append(create_tag)


@pytest.fixture(autouse=True, scope="session")
def append_ingredient(ingredient_list, create_ingredient):
    return ingredient_list.append(create_ingredient)


@pytest.fixture(scope="session")
def create_recipe(django_db_blocker, create_user, ingredient_list, tag_list) -> Recipe:
    with django_db_blocker.unblock():
        recipe = Recipe.objects.create(
            name="test",
            description="test",
            preparation_time="2023-04-19T10:51:01.889Z",
            cuisson_time="2023-04-19T10:51:01.889Z",
            user=create_user,
        )
        recipe.ingredients.set(ingredient_list)
        recipe.tags.set(tag_list)
        return recipe


@pytest.fixture(scope="session")
def create_recipe_list(django_db_blocker, create_recipe) -> List[Recipe]:
    recipe_list: List[Recipe] = []
    with django_db_blocker.unblock():
        recipe_list.append(create_recipe)
        return recipe_list


@pytest.fixture(scope="session")
def create_user_list(django_db_blocker) -> List[User]:
    user_list: List[User] = []
    with django_db_blocker.unblock():
        user_list.append(User.objects.create(username="royd"))
        user_list.append(User.objects.create(username="kartin"))
        return user_list
