from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes.views import TagViewSet, IngredientViewSet, RecipeViewSet

router_v1 = DefaultRouter()
router_v1.register('tags', TagViewSet, basename="tag_api")
router_v1.register('ingredients', IngredientViewSet, basename="ingredient_api")
router_v1.register('recipes', RecipeViewSet, basename='recipe_api')


urlpatterns = [
    path('', include(router_v1.urls)),
]