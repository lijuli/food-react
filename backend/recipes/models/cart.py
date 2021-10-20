from django.db import models

from recipes.models.recipe import Recipe
from users.models import User


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        related_name='cart_user',
        on_delete=models.CASCADE,
    )
    recipes = models.ForeignKey(
        Recipe,
        related_name='cart_recipe',
        verbose_name='recipe',
        help_text='select a recipe',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Shopping cart'
        verbose_name_plural = 'Shopping carts'

