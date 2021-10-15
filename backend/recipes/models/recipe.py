from django.db import models
from django.core.validators import MinValueValidator

from recipes.models.ingredient import Ingredient
from recipes.models.tag import Tag
from users.models import User


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name='author',
        on_delete=models.SET_NULL,
        null=True
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='ingredients',
        verbose_name='ingredients',
        through='RecipeIngredient',
        blank=False,
        help_text='select an ingredient'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=False,
        related_name='tags',
        verbose_name='tag',
        help_text='select a tag'
    )
    image = models.ImageField(
        upload_to='recipes/',
        max_length=None,
        # allow_empty_file=False
    )
    name = models.CharField(
        'recipe name',
        max_length=200,
        help_text='enter the recipe name'
    )
    text = models.TextField(
        'recipe text',
        blank=True,
        null=True,
        help_text='enter recipe here'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'cooking time',
        validators=[MinValueValidator(
            limit_value=1,
            message='You can not save time while cooking.'
        )]
    )
    pub_date = models.DateTimeField(
        verbose_name='published',
        auto_now_add=True,
        db_index=True
    )
    # is_favorited = models.BooleanField(default=False)
    # is_in_shopping_cart = models.BooleanField(default=False)

    # @property
    # def is_in_shopping_cart(self):
    #     try:
    #         return Cart.objects.exists(recipe=self)
    #     except Cart.DoesNotExist:
    #         return False
    #
    # @property
    # def is_favorited(self):
    #     try:
    #         return Favourite.objects.exists(recipe=self)
    #     except Favourite.DoesNotExist:
    #         return False
    #
    # class Meta:
    #     ordering = ('-pk',)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredients = models.ForeignKey(
        Ingredient,
        related_name='recipe_ingredients',
        on_delete=models.CASCADE,
    )
    recipes = models.ForeignKey(
        Recipe,
        related_name='recipe',
        on_delete=models.CASCADE,
    )
    amount = models.FloatField(
        validators=[MinValueValidator(limit_value=0.1)],
        null=False
    )

