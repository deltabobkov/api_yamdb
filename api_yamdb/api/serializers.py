import secrets
import string

from django.core.mail import send_mail
from rest_framework import serializers
from users.models import CHOICES, User


def generate_confirm_code():
    alphabet = string.ascii_letters + string.digits
    confirm_code = ''.join(secrets.choice(alphabet) for i in range(10))
    return confirm_code


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
        confirm_code = confirm_code
        message = (
            f"user: {validated_data['username']}\n"
            f"confirm code: {str(confirm_code)}"
        )
        to_email = user.email
        send_mail(
            'Activate your account.',
            message,
            'no-replay@yamdb.com',
            [to_email],
            fail_silently=False,
        )
        return user
