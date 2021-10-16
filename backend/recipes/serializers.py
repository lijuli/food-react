from drf_extra_fields.fields import Base64ImageField
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


# class Base64ImageField(serializers.ImageField):
#
#     def to_internal_value(self, data):
#         from django.core.files.base import ContentFile
#         import base64
#         import six
#         import uuid
#
#         if isinstance(data, six.string_types):
#             if 'data:' in data and ';base64,' in data:
#                 header, data = data.split(';base64,')
#
#             try:
#                 decoded_file = base64.b64decode(data)
#             except TypeError:
#                 self.fail('invalid_image')
#
#             file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
#             file_extension = self.get_file_extension(file_name, decoded_file)
#             complete_file_name = "%s.%s" % (file_name, file_extension, )
#             data = ContentFile(decoded_file, name=complete_file_name)
#
#         return super(Base64ImageField, self).to_internal_value(data)
#
#     def get_file_extension(self, file_name, decoded_file):
#         import imghdr
#
#         extension = imghdr.what(file_name, decoded_file)
#         extension = "jpg" if extension == "jpeg" else extension
#
#         return extension


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
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    image = Base64ImageField(max_length=None, use_url=True)

    tags = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Tag.objects.all(),
        # many=True
    )
    ingredients = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Ingredient.objects.all(),
        many=True
    )

    class Meta:
        model = Recipe
        # fields = '__all__'
        exclude = ('id',)
