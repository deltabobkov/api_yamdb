from rest_framework import routers
from .views import UserViewSet, ReviewViewSet, CommentViewSet

from django.urls import include, path

from .views import UserViewSet, auth, signup

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', auth, name='auth'),
    path('v1/', include(router.urls)),
]
