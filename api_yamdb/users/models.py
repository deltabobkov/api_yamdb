from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator

CHOICES = (
    (1, "admin"),
    (2, "user"),
    (3, "moderator")
)


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email and username.
        """
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_unusable_password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        if password is None:
            raise TypeError('Password should not be none')
        user = self.create_user(
            username,
            email,
            password,
        )
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9]*$',
                message='Username must be Alphanumeric',
                code='invalid_username'
            ),
        ]
    )
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=254,
        unique=True,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.IntegerField(
        choices=CHOICES,
        default=2,
        null=True,
        blank=True
    )
    is_verified = models.BooleanField(default=False),
    confirm_code = models.CharField(max_length=20, null=True, blank=True)

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
