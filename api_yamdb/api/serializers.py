from rest_framework import serializers
from users.models import CHOICES, User
from users.utils import generate_confirm_code, mail_send


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
        confirm_code = generate_confirm_code()
        user = User.objects.create(**validated_data, confirm_code=confirm_code)
        user = User.objects.create(**validated_data)

        confirm_code = confirm_code
        message = (
            f"user: {user.username}\n"
            f"confirm code: {str(user.confirm_code)}"
        )
        mail_send(
            subject="Confirmation code",
            message=message,
            sender='no-replay@yamdb.com',
            recipients=[user.email]
        )
        return user
