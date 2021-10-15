from django.db import models

from users.models import User
from recipes.models.recipe import Recipe


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
        on_delete = models.CASCADE,
    )

    class Meta:
        ordering = ('-pk',)

