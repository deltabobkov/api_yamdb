from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from users.utils import generate_confirm_code, mail_send

from django.shortcuts import get_object_or_404

from reviews.models import Category, Comment, Genre, Review, Title


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'bio',
            'role',
        )

    def create(self, validated_data):
        user = User.objects.create(
            **validated_data, confirm_code=generate_confirm_code()
        )
        return user

    def update(self, instance, validated_data):
        if validated_data.get('role'):
            validated_data.pop('role')
        return super().update(instance, validated_data)


class SingupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )

    def create(self, validated_data):
        user = User.objects.create(
            **validated_data, confirm_code=generate_confirm_code()
        )
        message = (
            f'Username: {user.username}\n'
            f'Confirmation code: {user.confirm_code}\n'
        )
        mail_send(
            subject="Confirmation code",
            message=message,
            sender='no-replay@yamdb.com',
            recipients=[user.email],
        )
        return user

    def update(self, instance, validated_data):
        instance.confirm_code = generate_confirm_code()
        instance.save()
        message = (
            f'Username: {instance.username}\n'
            f'Confirmation code: {instance.confirm_code}\n'
        )
        mail_send(
            subject="Confirmation code",
            message=message,
            sender='no-replay@yamdb.com',
            recipients=[instance.email],
        )
        return super().update(instance, validated_data)


class AuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    confirmation_code = serializers.CharField(
        read_only=True, source='confirm_code'
    )
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code', 'token')

    def create(self, validated_data):
        user = get_object_or_404(User, **validated_data)
        if user.confirm_code != validated_data.get("confirmation_code"):
            raise PermissionDenied('Код подтверждния или учетная запись')
        token = AccessToken.for_user(user)
        return token


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(slug_field='text', read_only=True)

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'review', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError(
                    'Вы не можете добавить более'
                    'одного отзыва на произведение'
                )
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'title', 'score', 'pub_date')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )


class TitlesPostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class TitlesGetSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        model = Title
