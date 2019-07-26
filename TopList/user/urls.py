from django.conf.urls import url
from django.urls import include
from rest_framework.routers import SimpleRouter

from authentication import views
from user.views import UserViewSet

router = SimpleRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    url('/', include(router.urls))
]
