from django.urls import include, path
from rest_framework.routers import SimpleRouter

from social.views import RecommendationListViewSet

router = SimpleRouter()
router.register('', RecommendationListViewSet, basename='social')

urlpatterns = [
    path('social/', include(router.urls))
]
