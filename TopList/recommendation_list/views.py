from django.db import transaction
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from recommendation_list.filters import CustomRecommendationListFieldsFilter, CustomTagFilter
from recommendation_list.models.recommendations import RecommendationList, Favorites, CategoryEnum
from recommendation_list.models.tags import Tag
from recommendation_list.permissions import IsOwnerOrReadOnly
from recommendation_list.serializers.recommendations_serializers import RecommendationListSerializer, \
    FavoritesSerializer
from recommendation_list.serializers.tags_serializers import TagSerializer


class RecommendationListViewSet(ModelViewSet):
    queryset = RecommendationList.objects.all()
    serializer_class = RecommendationListSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filterset_class = CustomRecommendationListFieldsFilter

    # @transaction.atomic
    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user
        return super().create(request, *args, **kwargs)

    @action(methods=['GET'], detail=False)
    def categories(self, request):
        return Response([elem.value for elem in CategoryEnum])


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = CustomTagFilter


class FavoritesViewSet(ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
