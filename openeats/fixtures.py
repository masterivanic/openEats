from typing import List

import pytest
from django.contrib.auth.models import User

from recipe.models import Ingredient
from recipe.models import Recipe
from recipe.models import Tag


@pytest.fixture(scope="module")
def create_user(django_db_blocker) -> User:
    with django_db_blocker.unblock():
        return User.objects.create(username="Nextjs", email="next@gmail.com")


@pytest.fixture(scope="module")
def create_ingredient(django_db_blocker) -> Ingredient:
    with django_db_blocker.unblock():
        return Ingredient.objects.create(
            name="Mayonnaise", description="très degoutant"
        )


@pytest.fixture(scope="module")
def create_ingredients_list(django_db_blocker) -> List[Ingredient]:
    with django_db_blocker.unblock():
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


@pytest.fixture(scope="module")
def create_tag_list(db) -> List[Tag]:
    """"""
    tag_list: List[Tag] = []
    tag_list.append(Tag.objects.create(name="tag1", description="nothing to say"))
    tag_list.append(Tag.objects.create(name="tag2", description="nothing to say"))
    tag_list.append(Tag.objects.create(name="tag3", description="nothing to say"))
    return tag_list


@pytest.fixture(scope="module")
def create_recipe(db, create_user) -> Recipe:
    """"""
    recipe = Recipe(
        name="test",
        description="test",
        preparation_time="2023-04-19T10:51:01.889Z",
        cuisson_time="2023-04-19T10:51:01.889Z",
        user=create_user,
    )
    return recipe


def test_ingredient_filter(create_ingredient) -> None:
    assert Ingredient.objects.filter(name="Mayonnaise").exists()
