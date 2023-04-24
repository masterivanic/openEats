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


class SearchSerializer(serializers.Serializer):
    ingredient_name = serializers.CharField(max_length=200, required=False)
    tag_name = serializers.CharField(max_length=200, required=False)
    name = serializers.CharField(max_length=200, required=False)


class RecipeDetailsSerializer(serializers.ModelSerializer):
    """RecipeDetails seriliazer in json"""

    ingredient = IngredientSerializer(many=True)
    tag = TagSerializer(many=True)

    class Meta:
        model = Recipe
        fields = [
            "name",
            "description",
            "preparation_time",
            "cuisson_time",
            "user",
            "ingredient",
            "tag",
        ]

    def create(self, validated_data) -> Recipe:
        """
        :param validated_data: get dict data from key of our instance
        return complete object instances based on the validated data
        """

        ingredients_data = validated_data.pop("ingredient")
        tag_data = validated_data.pop("tag")

        recipe = Recipe.objects.create(**validated_data)
        ingredients = [Ingredient(recipe, **data) for data in ingredients_data]
        tags = [Tag(recipe, **data) for data in tag_data]
        Ingredient.objects.bulk_create(ingredients)
        Tag.objects.bulk_create(tags)

        return recipe
