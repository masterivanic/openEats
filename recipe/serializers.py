from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Recipe
from ingredient.serializers import IngredientSerializer
from tag.serializers import TagSerializer


class UserSerializer(serializers.ModelSerializer):
    """User seriliazer in json"""

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}


class RecipeSerializer(serializers.ModelSerializer):
    """Recipe seriliazer in json"""

    class Meta:
        model = Recipe
        fields = "__all__"


class RecipeDetailsSerializer(serializers.ModelSerializer):
    """RecipeDetails seriliazer in json"""

    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = (
            "name",
            "description",
            "preparation_time",
            "cuisson_time",
            "user",
            "ingredients",
            "tags",
        )
