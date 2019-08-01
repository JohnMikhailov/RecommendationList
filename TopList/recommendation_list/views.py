from rest_framework.viewsets import ModelViewSet

from recommendation_list.models.recommendations import RecommendationList, Favorites
from recommendation_list.serializers.recommendations_serializers import RecommendationListSerializer, FavoritesSerializer

from rest_framework import filters


class RecommendationListViewSet(ModelViewSet):
    queryset = RecommendationList.objects.all()
    serializer_class = RecommendationListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user_id']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoritesViewSet(ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
