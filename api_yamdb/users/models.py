from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models

CHOICES = (
    ("admin", "admin"),
    ("user", "user"),
    ("moderator", "moderator")
)


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and username.
        """
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')
        if username == 'me':
            raise TypeError('Users not may username me')
        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )
        user.set_unusable_password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        if password is None:
            raise TypeError('Password should not be none')
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')
        if username == 'me':
            raise TypeError('Users not may username me')
        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.is_admin = True
        user.is_superuser
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    username = models.CharField(
        max_length=150,
        unique=True,
        null=False,
        blank=False,
        validators=[
            RegexValidator(
                regex='^(?!^me$)[\w.@+-]+$',
                message='Username must be Alphanumeric',
                code='invalid_username'
            )
        ]
    )
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    email = models.EmailField(
        max_length=254,
        verbose_name='email address',
        unique=True,
        null=False,
        blank=False,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True
    )
    role = models.CharField(
        max_length=50,
        choices=CHOICES,
        default="user",
        null=True,
        blank=True
    )
    confirm_code = models.CharField(max_length=20, null=True, blank=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
