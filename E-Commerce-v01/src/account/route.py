from rest_framework import routers
from .auth import UserModelViewSet

router = routers.DefaultRouter()
router.register('users', UserModelViewSet, basename='users')
