from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
