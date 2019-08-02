from django.urls import include, path
from rest_framework.routers import SimpleRouter

from recommendation_list.views import RecommendationListViewSet, FavoritesViewSet

router = SimpleRouter()
router.register('recommendations', RecommendationListViewSet, basename='recommendation_list')
router.register('favorites', FavoritesViewSet, basename='favorites')

urlpatterns = [
    path('', include(router.urls)),
]
