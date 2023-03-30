from rest_framework import viewsets
from users.models import User
from .serializers import UserSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        if self.request.user.role != 1:
            raise PermissionDenied(
                'Не достаточно прав для создания пользователя!')
        super(UserViewSet, self).perform_create(serializer)

    def perform_update(self, serializer):
        if self.request.user.is_superuser != 1:
            raise PermissionDenied(
                'Не достаточно прав для создания пользователя!')
        super(UserViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if self.request.user.is_superuser != 1:
            raise PermissionDenied(
                'Не достаточно прав для создания пользователя!')
        return super().perform_destroy(instance)
