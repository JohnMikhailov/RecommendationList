from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from recommendation_list.filters import CategoryFilter
from recommendation_list.models.recommendations import RecommendationList, Favorites, CategoryEnum
from recommendation_list.serializers.recommendations_serializers import RecommendationListSerializer, \
    FavoritesSerializer


class RecommendationListViewSet(ModelViewSet):
    queryset = RecommendationList.objects.all()
    serializer_class = RecommendationListSerializer

    permission_classes = [AllowAny]
    filterset_class = CategoryFilter

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user
        return super().create(request, *args, **kwargs)

    @action(methods=['GET'], detail=False)
    def categories(self, request):
        return Response([elem.value for elem in CategoryEnum])


class FavoritesViewSet(ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
