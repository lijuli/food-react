from django.db import models

from recipes.models import Recipe
from users.models import User


class Favourite(models.Model):
    user = models.ForeignKey(
        User,
        related_name='fav_user',
        on_delete=models.CASCADE,
    )

    recipe = models.ForeignKey(
        Recipe,
        related_name='fav_recipe',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Favourite recipe'
        verbose_name_plural = 'Favourite recipes'

