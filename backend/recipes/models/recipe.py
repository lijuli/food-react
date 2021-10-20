from django.core.validators import MinValueValidator
from django.db import models

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
        help_text='select an ingredient'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
        verbose_name='tag',
        help_text='select a tag'
    )
    image = models.ImageField(
        upload_to='recipes/',
        max_length=None,
    )
    name = models.CharField(
        'recipe name',
        max_length=200,
        help_text='enter the recipe name'
    )
    text = models.TextField(
        'recipe text',
        blank=True,
        help_text='enter recipe here'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'cooking time',
        help_text='(in minutes)',
        validators=(MinValueValidator(
            limit_value=1,
            message='You can not save time while cooking.'
        ),)
    )
    pub_date = models.DateTimeField(
        verbose_name='published',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

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
        validators=(MinValueValidator(
            limit_value=0.1,
            message='Ingrediant amount cannot be zero or negative.'
        ),),
        null=False
    )

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Ingredient for Recipe'
        verbose_name_plural = 'Ingredients for Recipe'

    def __str__(self):
        return f'{self.ingredients.name} - {self.amount}'
