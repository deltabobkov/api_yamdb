from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from users.permissions import IsAdmin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from reviews.models import Title, Review
from django.shortcuts import get_object_or_404

from .serializers import SingupSerializer, UserSerializer, ReviewSerializer, CommentSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    lookup_field = ('username')
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']


@api_view(['POST'])
@permission_classes([AllowAny])
def auth(request):
    if request.method != 'POST':
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if not request.data.get("username") or request.data.get("username") == "":
        return Response(status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, username=request.data.get("username"))
    if user.confirm_code != request.data.get("confirmation_code"):
        raise ParseError('Код подтверждния или учетная запись')

    token = AccessToken.for_user(user)

    return Response({"token": f"{token}"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    if not User.objects.filter(username=request.data.get("username")).exists():
        serializer = SingupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        if User.objects.filter(username=request.data.get("username"),
                               email=request.data.get("email")).exists():
            user = User.objects.get(username=request.data.get("username"),
                                    email=request.data.get("email"))
            serializer = SingupSerializer(user,
                                          data=request.data,
                                          partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
    return Response("Bad request", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH'])
def selfuser(request):
    user = request.user

    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        if request.method == 'PATCH':
            serializer.save()
        return Response(serializer.data)
    raise ValidationError(serializer.errors)


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

