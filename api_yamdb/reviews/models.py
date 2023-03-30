from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        'Имя категории',
        max_length=200
    )
    slug = models.SlugField('Категория', max_length=100, unique=True,)

    class Meta:
        verbose_name = 'Категория'


class Genre(models.Model):
    name = models.CharField(
        'Имя жанра',
        max_length=200
    )
    slug = models.SlugField('Жанр', max_length=100, unique=True,)

    class Meta:
        verbose_name = 'Жанр'


class Titles(models.Model):
    name = models.CharField(
        'Имя жанра',
        max_length=200
    )
    year = models.IntegerField('год')
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, related_name='genre', null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='category', null=True)

    class Meta:
        verbose_name = 'Произведение'

    def __str__(self):
        return self.name
