from rest_framework import serializers
from users.models import CHOICES, User
from users.utils import generate_confirm_code


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=CHOICES, required=False)

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
