from rest_framework import routers

from django.urls import include, path

from .views import UserViewSet, auth, signup

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', auth, name='auth'),
    path('v1/', include(router.urls)),
]
