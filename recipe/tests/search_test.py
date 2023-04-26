from django.db.models import Q
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from recipe.models import Recipe
from recipe.serializers import RecipeDetailsSerializer


class SearchTestAPI(APITestCase):
    """search api endpoint testing (to do before wrinting our views)"""

    def test_that_user_can_filter_recipe_using_name_recipe(self) -> None:
        params = {"name": "su"}
        recipe = Recipe.objects.filter(name__icontains=params["name"])
        serializer = RecipeDetailsSerializer(recipe, many=True)
        factory = self.client.get(reverse("recipe-search"), {"name": "Sushi"})
        factory1 = self.client.get(reverse("recipe-search"), params)

        assert factory.status_code == status.HTTP_200_OK
        assert factory1.status_code == status.HTTP_200_OK
        self.assertEqual(factory.data, serializer.data)
        self.assertEqual(factory1.data, serializer.data)

    def test_that_user_can_filter_recipe_using_ingredient(self) -> None:
        params = {"ingredient_name": "farine"} or {"ingredient_name": "Fa"}
        recipe = Recipe.objects.filter(
            ingredient__name__icontains=params["ingredient_name"]
        )
        serializer = RecipeDetailsSerializer(recipe, many=True)

        response = self.client.get(reverse("recipe-search"), params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), len(serializer.data))

    def test_that_user_can_filter_recipe_using_tag(self) -> None:
        params = {"tag_name": "Halal"} or {"tag_name": "ha"}
        recipe = Recipe.objects.filter(tag__name__icontains=params["tag_name"])
        serializer = RecipeDetailsSerializer(recipe, many=True)

        response = self.client.get(reverse("recipe-search"), params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_that_user_can_filter_recipe_combining_two_filters(self) -> None:
        params = {"tag_name": "Halal", "ingredient_name": "Fa"}
        recipe = Recipe.objects.filter(
            Q(tag__name__icontains=params["tag_name"]),
            Q(ingredient__name__icontains=params["ingredient_name"]),
        )
        serializer = RecipeDetailsSerializer(recipe, many=True)
        response = self.client.get(reverse("recipe-search"), params)

        assert response.status_code == status.HTTP_200_OK
        self.assertEqual(response.data, serializer.data)

    def test_that_user_can_filter_recipe_combining_tree_filters(self) -> None:
        params = {"ingredient_name": "Fa", "name": "hello", "tag_name": "Fa"}
        recipe = Recipe.objects.filter(
            Q(tag__name__icontains=params["tag_name"]),
            Q(ingredient__name__icontains=params["ingredient_name"]),
            Q(name__icontains=params["name"]),
        )
        response = self.client.get(reverse("recipe-search"), params)
        serializer = RecipeDetailsSerializer(recipe, many=True)

        assert response.status_code == status.HTTP_200_OK
        self.assertEqual(response.data, serializer.data)
