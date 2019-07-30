from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from TopList import settings
from user.views import UserViewSet

# DefaultRouter()?
router = SimpleRouter()
router.register('', UserViewSet, basename='users')

urlpatterns = [
    path('users/', include(router.urls))
]
