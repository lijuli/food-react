from django.contrib import admin

from recipes.models import Recipe
from recipes.models import Ingredient
from recipes.models import Tag
from recipes.models import Favourite
from recipes.models import Cart


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'cooking_time')
    search_fields = ('name', 'ingredients',)
    list_filter = ('cooking_time',)
    readonly_fields = ('author',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('id', 'name')
    list_filter = ('name', 'measurement_unit',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('slug',)


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('recipe',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipes')
    search_fields = ('user', 'recipes')
    list_filter = ('user',)
