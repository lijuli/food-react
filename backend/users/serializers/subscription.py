from recipes.models import Recipe
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import Subscription, User
from users.serializers.user import CustomUserSerializer


class SubscribeSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField('get_recipes')
    recipes_count = serializers.SerializerMethodField('get_recipes_count')

    class Meta:
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',
                  'recipes',
                  'recipes_count',)
        model = User
        validators = (
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('user', 'subscribed')
            ),
        )

    def validate(self, data):
        user = self.context.get('request').user
        subscribed = data.get('subscribed')
        if user == subscribed:
            raise serializers.ValidationError(
                "Users can't subscribe to themselves."
            )
        return data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    def get_recipes(self, obj):
        if 'recipes_limit' in self.context.get('request').query_params:
            recipes_limit = int(self.context.get(
                'request'
            ).query_params.get('recipes_limit'))
            serializer = RecipeSubscriptionSerializer(
                Recipe.objects.filter(author=obj)[:recipes_limit],
                many=True
            )
        else:
            serializer = RecipeSubscriptionSerializer(
                Recipe.objects.filter(author=obj),
                many=True
            )
        return serializer.data


class RecipeSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
