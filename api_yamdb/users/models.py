from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        (1, 'admin'),
        (2, 'user'),
        (3, 'moderator')
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    ),
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username
