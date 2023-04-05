from django.urls import include, path
from rest_framework import routers
from .views import ReviewViewSet, CommentViewSet, TitleViewSet, GenreViewSet, UserViewSet, auth, signup, CategoryViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(
    r'categories',
    CategoryViewSet,
    basename='category',
)
router.register(
    r'genres',
    GenreViewSet,
    basename='genre',
)
router.register(
    r'titles',
    TitleViewSet,
    basename='title',
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', auth, name='auth'),
]
