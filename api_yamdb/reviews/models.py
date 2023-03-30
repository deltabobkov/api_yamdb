from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()

class Title(models.Model):
    pass


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='review'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='review'
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
