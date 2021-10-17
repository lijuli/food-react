from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action

from recipes.models.recipe import Recipe, RecipeIngredient
from recipes.models.tag import Tag
from recipes.models.ingredient import Ingredient
from recipes.models.favourite import Favourite
from recipes.models import Cart
from users.serializers.user import CustomUserSerializer
from users.serializers.subscription import RecipeSubscriptionSerializer


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        # fields = '__all__'
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
            return RecipeIngredient.objects.filter(ingredients=obj).values_list('amount')[0][0]
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
    is_favorited = serializers.SerializerMethodField('get_is_favorited')
    is_in_shopping_cart = serializers.SerializerMethodField('get_is_in_shopping_cart')

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
            return Favourite.objects.filter(recipe=obj).exists()
        except Favourite.DoesNotExist:
            return False

    def get_is_in_shopping_cart(self, obj):
        try:
            return Cart.objects.filter(recipes=obj, user=self.context['request'].user).exists()
        except Cart.DoesNotExist:
            return False


class RecipeWriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True)
    ingredients = RecipeIngredientSerializer(many=True)
    cooking_time = serializers.IntegerField()

    def create(self, validated_data):
        author = self.context['request'].user
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')

        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags_data)  # Direct assignment to the forward side of a many-to-many set is prohibited. Use tags.set() instead.
        recipe.save()

        for ingredient in ingredients_data:
            ingredient_dictionary = dict(ingredient)
            RecipeIngredient.objects.create(
                recipes=recipe,
                ingredients=Ingredient.objects.get(id=ingredient_dictionary['id']),
                amount=ingredient['amount']
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
                ingredients=Ingredient.objects.get(id=ingredient_dictionary['id']),
                amount=ingredient['amount']
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