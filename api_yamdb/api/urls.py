from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet, ReviewViewSet, CommentViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
