from django.shortcuts import get_object_or_404
from django.db.models import Sum

from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from users.models import User
from recipes.models import Cart
from recipes.models.recipe import Recipe
from recipes.models.tag import Tag
from recipes.models.ingredient import Ingredient
from recipes.models.favourite import Favourite
from recipes.serializers import (
    TagSerializer,
    IngredientSerializer,
    FavouriteSerializer,
    RecipeWriteSerializer,
    RecipeListSerializer,
    CartSerializer,
)


class TagViewSet(ModelViewSet):
    """A ViewSet for viewing Tag instances."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = PageNumberPagination
    # permission_classes = (IsAdminOrReadOnly,)
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('name',)
    # lookup_field = 'slug'

    def get_paginated_response(self, data):
        return Response(data)


class IngredientViewSet(ModelViewSet):
    """A ViewSet for viewing Ingredient instances."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = PageNumberPagination
    # permission_classes = (IsAdminOrReadOnly,)
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('name',)
    # lookup_field = 'slug'

    def get_paginated_response(self, data):
        return Response(data)


# class FavouriteViewSet(ModelViewSet):
#     queryset = Favourite.objects.all()
#     serializer_class = FavouriteSerializer
#     # pagination_class = PageNumberPagination
#     # permission_classes = (IsAdminOrReadOnly,)
#     # filter_backends = (filters.SearchFilter,)
#     # search_fields = ('name',)
#     # lookup_field = 'slug'
#
#     # def get_paginated_response(self, data):
#     #     return Response(data)
#
#     # def get_queryset(self):
#     #     return Favourite.objects.filter(recipe=self.kwargs['recipe_id'])
#     #
#     # def perform_create(self, serializer):
#     #     recipe = get_object_or_404(Recipe, id=self.kwargs['recipe_id'])
#     #     serializer.save(author=self.request.user, recipe=recipe)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    # permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['group']

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return RecipeListSerializer
        return RecipeWriteSerializer

    # @action(
    #     detail=True,
    #     methods=['get'],
    #     url_path='download_shopping_cart'
    # )
    # def download_shopping_cart(self, request, *args, **kwargs):
    #     # current_user = self.request.user
    #     result_ingr = Recipe.objects.all()
    #
    #     serializer = RecipeListSerializer(
    #         instance=result_ingr,
    #         many=True
    #     )
    #     return Response(serializer.data, status=status.HTTP_200_OK)

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
                data={
                    'user': current_user.id,
                    'recipe': recipe.id
                },
                context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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


