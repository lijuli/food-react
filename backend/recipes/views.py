from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.filters import IngredientsFilter, RecipesFilter
from recipes.models import (Cart, Favourite, Ingredient, Recipe,
                            RecipeIngredient, Tag)
from recipes.permissions import IsAdmin
from recipes.serializers import (CartSerializer, FavouriteSerializer,
                                 IngredientSerializer, RecipeListSerializer,
                                 RecipeWriteSerializer, TagSerializer)
from users.serializers.subscription import RecipeSubscriptionSerializer


class DefaultResultsSetPagination(PageNumberPagination):
    """A Custom pagination class."""
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 10


class TagViewSet(ReadOnlyModelViewSet):
    """A ViewSet for viewing Tag instances."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = DefaultResultsSetPagination
    permission_classes = [AllowAny]

    def get_paginated_response(self, data):
        return Response(data)


class IngredientViewSet(ReadOnlyModelViewSet):
    """A ViewSet for viewing Ingredient instances."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = DefaultResultsSetPagination
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientsFilter
    filter_fields = ('name',)

    def get_paginated_response(self, data):
        return Response(data)


class RecipeViewSet(ModelViewSet):
    """A ViewSet for creating, editing and viewing Recipe instances."""
    queryset = Recipe.objects.all()
    pagination_class = DefaultResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipesFilter
    filter_fields = ('tags', 'is_favorited', 'is_in_shopping_cart',)

    def get_permissions(self):
        if self.action in ('create', 'partial_update', 'update', 'destroy'):
            self.permission_classes = [IsAuthenticated, IsAdmin]
        if self.action in ('list', 'retrieve'):
            self.permission_classes = [AllowAny]
        elif self.action in (
                'favorite', 'add_to_shopping_cart', 'download_shopping_cart'
        ):
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return RecipeListSerializer
        return RecipeWriteSerializer

    @action(
        detail=False,
        methods=['get'],
        url_path='download_shopping_cart'
    )
    def download_shopping_cart(self, request, *args, **kwargs):
        current_user = request.user
        recipes_ids = Cart.objects.filter(
            user=current_user
        ).values_list('recipes_id', flat=True)
        ingredients = list(RecipeIngredient.objects.filter(
            recipes_id__in=recipes_ids
        ).values_list(
            'ingredients__name',
            'ingredients__measurement_unit',
            'amount',
        ))
        shopping_list = [f'{ingredient[0]}({ingredient[1]}) - {ingredient[2]}'
                         + '\n' for ingredient in ingredients]
        return HttpResponse(shopping_list, content_type='text/plain')

    @staticmethod
    def return_resp(serializer):
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=True,
        methods=['get', 'delete'],
        url_path='favorite'
    )
    def favorite(self, request, pk=None):
        current_user = self.request.user
        recipe = get_object_or_404(
            Recipe,
            id=pk
        )

        if request.method == 'GET':
            if Favourite.objects.filter(recipe=recipe).exists():
                return Response(status=status.HTTP_204_NO_CONTENT)
            serializer = FavouriteSerializer(
                required=False,
                data={'user': current_user.id, 'recipe': recipe.id},
                context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        Favourite.objects.filter(user=current_user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['get', 'delete'],
        url_path='shopping_cart'
    )
    def add_to_shopping_cart(self, request, pk=None):
        current_user = request.user
        recipe = get_object_or_404(
            Recipe,
            id=pk
        )

        if request.method == 'GET':
            if Cart.objects.filter(recipes=recipe).exists():
                return Response(status=status.HTTP_204_NO_CONTENT)
            serializer = CartSerializer(
                many=False,
                instance=recipe,
                context={'request': request}
            )
            Cart.objects.create(user=current_user, recipes=recipe)
            return Response(serializer.data, status=status.HTTP_200_OK)

        Cart.objects.filter(user=current_user, recipes=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
