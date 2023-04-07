from django_filters.rest_framework import (
    CharFilter,
    DjangoFilterBackend,
    FilterSet,
)
from rest_condition import Or
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from .permissions import IsAdmin, IsAuthorOrReadOnly, NonAuth, ReadOnly

from django.db.models import Avg
from django.shortcuts import get_object_or_404

from reviews.models import Category, Genre, Review, Title

from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    SingupSerializer,
    TitlesGetSerializer,
    TitlesPostSerializer,
    UserSerializer,
)
from users.utils import generate_confirm_code, mail_send


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='me',
        permission_classes=(IsAuthenticated,),
    )
    def selfuser(self, request):
        serializer = UserSerializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            if request.method == 'PATCH':
                serializer.save()
            return Response(serializer.data)
        raise ValidationError(serializer.errors)


@api_view(['POST'])
@permission_classes([AllowAny])
def auth(request):
    if not request.data.get("username"):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, username=request.data.get("username"))
    if user.confirm_code != request.data.get("confirmation_code"):
        raise ParseError('Код подтверждния или учетная запись')

    token = AccessToken.for_user(user)

    return Response({"token": f"{token}"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    confirm_code = generate_confirm_code()
    data = {
        "confirm_code": confirm_code,
        "username": request.data.get('username'),
        "email": request.data.get('email')
    }
    user = User.objects.filter(
        username=request.data.get("username"),
        email=request.data.get("email"),
    ).first()
    if not user:
        serializer = SingupSerializer(data=data)
    else:
        serializer = SingupSerializer(user, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        message = (
            f'Username: {serializer.validated_data.get("username")}\n'
            f'Confirmation code: {confirm_code}\n'
        )
        mail_send(
            subject="Confirmation code",
            message=message,
            sender='no-replay@yamdb.com',
            recipients=[serializer.validated_data.get("email")],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        Or(IsAuthorOrReadOnly, NonAuth),
        IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.select_related("author")

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        Or(IsAuthorOrReadOnly, NonAuth),
        IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.select_related("author")

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)


class TitleSlugFilter(FilterSet):
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')

    class Meta:
        model = Title
        fields = ['name', 'year', 'category', 'genre']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = (
        Title.objects.annotate(Avg('reviews__score'))
        .select_related('category')
        .prefetch_related('genre')
        .order_by('name')
    )
    serializer_class = TitlesGetSerializer
    permission_classes = (Or(ReadOnly, IsAdmin),)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleSlugFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitlesGetSerializer
        return TitlesPostSerializer


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (Or(ReadOnly, IsAdmin),)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('^name',)
    lookup_field = 'slug'


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
    lookup_field = 'slug'
    permission_classes = (Or(ReadOnly, IsAdmin),)
