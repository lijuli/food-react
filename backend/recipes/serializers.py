from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

from recipes.fields import Base64ImageField
from recipes.models import (Cart, Favourite, Ingredient, Recipe,
                            RecipeIngredient, Tag)
from users.serializers.subscription import RecipeSubscriptionSerializer
from users.serializers.user import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class TagWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Tag
        fields = (
            'id',
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = '__all__'

    def to_representation(self, obj):
        recipe = get_object_or_404(Recipe, id=obj.recipe.id)
        if recipe:
            return RecipeSubscriptionSerializer(obj.recipe).data
        return super().to_representation(obj)


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

    def to_representation(self, obj):
        recipe = get_object_or_404(Recipe, id=obj.id)
        if recipe:
            return RecipeSubscriptionSerializer(obj).data
        return super().to_representation(obj)


class IngredientForRecipeSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField('get_amount')

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )

    def get_amount(self, obj):
        try:
            return RecipeIngredient.objects.filter(
                ingredients=obj
            ).values_list('amount')[0][0]
        except Favourite.DoesNotExist:
            return False


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)
    amount = serializers.FloatField(write_only=True)

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'amount',
        )


class RecipeListSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientForRecipeSerializer(read_only=True, many=True)
    tags = TagSerializer(read_only=True, many=True)
    is_favorited = serializers.SerializerMethodField(
        'get_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        'get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        try:
            if self.context.get('request').user.is_anonymous:
                return False
            return Favourite.objects.filter(
                recipe=obj,
                user=self.context.get('request').user
            ).exists()
        except Favourite.DoesNotExist:
            return False

    def get_is_in_shopping_cart(self, obj):
        try:
            if self.context.get('request').user.is_anonymous:
                return False
            return Cart.objects.filter(
                recipes=obj,
                user=self.context.get('request').user
            ).exists()
        except Cart.DoesNotExist:
            return False


class RecipeWriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True)
    ingredients = RecipeIngredientSerializer(many=True)
    cooking_time = serializers.IntegerField()

    def create(self, validated_data):
        author = self.context.get('request').user
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')

        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags_data)
        recipe.save()

        for ingredient in ingredients_data:
            ingredient_dictionary = dict(ingredient)
            RecipeIngredient.objects.create(
                recipes=recipe,
                ingredients=Ingredient.objects.get(
                    id=ingredient_dictionary.get('id')
                ),
                amount=ingredient.get('amount')
            )
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        for item in validated_data:
            if Recipe._meta.get_field(item):
                setattr(instance, item, validated_data[item])
        RecipeIngredient.objects.filter(recipes=instance).delete()
        for ingredient in ingredients_data:
            ingredient_dictionary = dict(ingredient)
            RecipeIngredient.objects.create(
                recipes=instance,
                ingredients=Ingredient.objects.get(
                    id=ingredient_dictionary.get('id')
                ),
                amount=ingredient.get('amount')
            )
        instance.tags.set(tags_data)
        instance.save()
        return instance

    class Meta:
        model = Recipe
        exclude = ('id',)

    def to_representation(self, obj):
        recipe = get_object_or_404(Recipe, id=obj.id)
        if recipe:
            return RecipeListSerializer(obj, context=self.context).data
        return super().to_representation(obj)
