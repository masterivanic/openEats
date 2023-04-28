from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from recipe.models import Recipe
from recipe.serializers import RecipeSerializer
from recipe.serializers import UserSerializer


class UserTestAPI(APITestCase):
    """User api endpoint test"""

    def test_user_listing(self) -> None:
        response = self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_creation(self) -> None:
        user_to_create = dict(
            username="Jean", email="jean@gmail.com", password="ceciestmonpass"
        )
        response = self.client.post(reverse("user-list"), data=user_to_create)
        user = User.objects.last()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.username, user_to_create["username"])

    def test_user_update(self) -> None:
        user_update = User.objects.all()[0:1]
        user_update[0].email = "invente@gmail.com"
        user_serializer = UserSerializer(data=user_update[0])
        if user_serializer.is_valid():
            response = self.client.put(
                reverse("user-list", args=[user_update[0].pk]), 
                user_serializer.data
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)


class RecipeTestAPI(APITestCase):
    """Recipe api endpoint test"""

    def test_user_listing(self) -> None:
        response = self.client.get(reverse("recipe-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_recipe_creation(self) -> None:
        user = User.objects.all()[0:1]
        recipe_to_create = Recipe(
            name="test",
            description="test",
            preparation_time="2023-04-19T10:51:01.889Z",
            cuisson_time="2023-04-19T10:51:01.889Z",
            user=user[0].pk
        )
        serializer_recipe = RecipeSerializer(recipe_to_create)

        response = self.client.post(
            reverse("recipe-list"), serializer_recipe.data
        )
        recipe = Recipe.objects.filter(name="test", description="test")[0:1]

        serializer = RecipeSerializer(recipe[0])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(serializer.data, serializer_recipe.data)

    def test_update_recipe(self) -> None:
        recipe = Recipe.objects.all()[0:1]
        recipe[0].description = "description test"
        recipe_serializer = RecipeSerializer(recipe[0])

        if recipe_serializer.is_valid():
            response = self.client.put(
                reverse("recipe-list", args=[recipe[0].pk]), 
                recipe_serializer.data
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
