from colorfield.fields import ColorField
from django.db import models


class Tag(models.Model):
    name = models.CharField(
        'tag name',
        max_length=200,
        help_text='enter the tag name'
    )
    color = ColorField(
        ColorField(default='#FF0000')
    )
    slug = models.SlugField(
        'tag reference label',
        unique=True,
        help_text='enter the tag reference label'
    )

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name
