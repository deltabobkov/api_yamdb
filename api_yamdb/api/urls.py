from rest_framework import routers

from django.urls import include, path

from .views import UserViewSet, auth, selfuser, singup

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/auth/singup/', singup, name='singup'),
    path('v1/auth/token/', auth, name='auth'),
    path('v1/users/me', selfuser, name='me'),
    path('v1/', include(router.urls)),
]
