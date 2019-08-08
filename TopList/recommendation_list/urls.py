from django.urls import include, path
from rest_framework.routers import SimpleRouter

from recommendation_list.views import RecommendationListViewSet, FavoritesViewSet, RecommendationViewSet

from rest_framework_nested import routers

router = SimpleRouter()
router.register('recommendations', RecommendationListViewSet, basename='recommendation_list')
router.register('favorites', FavoritesViewSet, basename='favorites')

recommendation_router = routers.NestedSimpleRouter(router, 'recommendations', lookup='recommendation_list')
recommendation_router.register('tips', RecommendationViewSet, basename='recommendation_detailing')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(recommendation_router.urls))
]
