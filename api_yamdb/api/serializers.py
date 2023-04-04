from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from users.utils import generate_confirm_code, mail_send

from django.shortcuts import get_object_or_404


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'bio',
            'role')

    def create(self, validated_data):
        user = User.objects.create(**validated_data,
                                   confirm_code=generate_confirm_code())
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
        user = User.objects.create(**validated_data,
                                   confirm_code=generate_confirm_code())
        message = (
            f'Username: {user.username}\n'
            f'Confirmation code: {user.confirm_code}\n'
        )
        mail_send(
            subject="Confirmation code",
            message=message,
            sender='no-replay@yamdb.com',
            recipients=[user.email]
        )
        return user

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

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
            recipients=[instance.email]
        )
        return super().update(instance, validated_data)


class AuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    confirmation_code = serializers.CharField(read_only=True,
                                              source='confirm_code')
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code',
            'token'
        )

    def create(self, validated_data):
        user = get_object_or_404(User, **validated_data)
        if user.confirm_code != validated_data.get("confirmation_code"):
            raise PermissionDenied('Код подтверждния или учетная запись')
        token = AccessToken.for_user(user)
        return token
