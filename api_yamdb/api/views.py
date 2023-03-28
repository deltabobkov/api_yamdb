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
        if not self.request.user.is_superuser:
            raise PermissionDenied(
                'Не достаточно прав для создания пользователя!')
        super(UserViewSet, self).perform_create(serializer)

    def perform_update(self, serializer):
        if not self.request.user.is_superuser:
            raise PermissionDenied(
                'Не достаточно прав для создания пользователя!')
        super(UserViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        instance = self.get_object()
        if self.request.user != instance.author:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        return super().perform_destroy(instance)
