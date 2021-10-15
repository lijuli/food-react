from django.db import models


class Ingredient(models.Model):
    name = models.CharField(
        'ingredient name',
        max_length=200,
        blank=False,
        null=False,
        help_text='enter the ingredient name'
    )
    measurement_unit = models.CharField(
        'ingredient measurement units',
        max_length=200,
        blank=False,
        null=False,
        help_text='enter measurement units'
    )

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return self.name
