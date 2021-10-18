import django_filters as filters

from recipes.models import Cart, Favourite, Ingredient, Recipe, Tag


class RecipesFilter(filters.FilterSet):
    author = filters.NumberFilter(field_name='author_id')
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        to_field_name='slug',
        field_name='tags__slug',
    )
    is_favorited = filters.BooleanFilter(
        method='filter_by_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_by_is_in_shopping_cart'
    )

    def filter_by_is_favorited(self, queryset, name, value):
        return queryset.filter(id__in=Favourite.objects.filter(
            user=self.request.user
        ).values_list('recipe_id', flat=True))

    def filter_by_is_in_shopping_cart(self, queryset, name, value):
        return queryset.filter(id__in=Cart.objects.filter(
            user=self.request.user
        ).values_list('recipes_id', flat=True))

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'is_favorited',
            'is_in_shopping_cart',
            'author'
        )


class IngredientsFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = ('name',)
