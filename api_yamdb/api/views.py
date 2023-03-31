from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import SlidingToken
from users.models import User
from users.permissions import IsAdmin
from users.utils import generate_confirm_code, mail_send

from django.shortcuts import get_object_or_404

from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'username'


@api_view(['POST'])
@permission_classes([AllowAny])
def auth(request):
    if request.method != 'POST':
        return Response(status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, username=request.data["username"])
    if user.confirm_code != request.data["confirmation_code"]:
        raise PermissionDenied('Код подтверждния или учетная запись')
    token = SlidingToken.for_user(user)
    return Response({"token": f"{token}"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def singup(request):
    if request.method != 'POST':
        return Response(status=status.HTTP_400_BAD_REQUEST)
    user, created = User.objects.get_or_create(
        username=request.data["username"],
        email=request.data["email"],
        defaults={'confirm_code': generate_confirm_code()}
    )
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
    return Response(
        {"email": f"{user.email}", "username": f"{user.username}"},
        status=status.HTTP_201_CREATED
    )


@api_view(['GET', 'PATCH'])
def selfuser(request):
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        if request.method == 'PATCH':
            serializer.save()
        return Response(serializer.data)
    raise ValidationError(serializer.errors)
