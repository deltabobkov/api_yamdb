from rest_framework import viewsets
from users.models import User
from reviews.models import Comment, Review
from .serializers import UserSerializer, CommentSerializer, ReviewSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404


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


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()
        
    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)

