
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator


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
        

class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='review'
    )
    title = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name='review'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    text = models.TextField('Текст отзыва')
    score = models.PositiveIntegerField(
        default=5, validators=[MaxValueValidator(10), MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Отзыв'
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    text = models.TextField(
        'Текст комментария',
    )
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created']

    def __str__(self) -> str:
        return self.text
