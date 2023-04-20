from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Ingredient
from .models import Recipe
from .models import Tag


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


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    """tag seriliazer in json"""

    class Meta:
        model = Tag
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
