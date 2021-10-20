from django.db import models


class Ingredient(models.Model):
    MEASUREMENT_UNITS = [
        ('g', 'gram'),
        ('kg', 'kilogram'),
        ('mg', 'milligram'),
        ('oz', 'ounce'),
        ('lb', 'pound'),
        ('tsp', 'teaspoon'),
        ('tbsp', 'tablespoon'),
        ('c', 'cup'),
        ('ml', 'milliliter'),
        ('l', 'liter'),
        ('cm', 'centimeter'),
        ('in', 'inch'),
        ('item', 'regular item'),
        ('piece', 'piece'),
        ('to taste', 'to taste'),
        ('drop', 'drop')
    ]

    name = models.CharField(
        'ingredient name',
        max_length=200,
        help_text='enter the ingredient name'
    )
    measurement_unit = models.CharField(
        'ingredient measurement units',
        max_length=200,
        choices=MEASUREMENT_UNITS,
        help_text='enter measurement units'
    )

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return self.name
