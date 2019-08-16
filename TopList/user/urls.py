from django.urls import include, path
from rest_framework.routers import SimpleRouter

from user.views import UserViewSet


router = SimpleRouter()
router.register('', UserViewSet, basename='users')

urlpatterns = [
    path('users/', include(router.urls)),
]
