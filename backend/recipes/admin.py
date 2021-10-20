from django.contrib import admin

from recipes.models.cart import Cart
from recipes.models.favourite import Favourite
from recipes.models.ingredient import Ingredient
from recipes.models.recipe import Recipe, RecipeIngredient
from recipes.models.tag import Tag


class IngredientInline(admin.TabularInline):
    model = RecipeIngredient

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline]

    def recipe_favorited_count(self, obj):
        return obj.fav_recipe.count()
    recipe_favorited_count.short_description = 'Favorited count'

    fields = ('author', 'name', 'text', 'tags', 'cooking_time', 'recipe_favorited_count')
    list_display = ('name', 'author')
    search_fields = ('name', 'ingredients',)
    list_filter = ('author', 'name', 'tags')
    readonly_fields = ('recipe_favorited_count',)
    empty_value_display = '-empty-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-empty-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('slug',)
    empty_value_display = '-empty-'


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('recipe',)
    empty_value_display = '-empty-'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipes')
    search_fields = ('user', 'recipes')
    list_filter = ('user',)
    empty_value_display = '-empty-'
