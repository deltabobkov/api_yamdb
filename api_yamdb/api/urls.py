from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet, auth, selfuser

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/users/me', selfuser, name='me'),
    path('v1/', include(router.urls)),
    path('v1/auth/token', auth, name='auth')
]
