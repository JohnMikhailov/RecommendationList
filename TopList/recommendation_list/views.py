from django.db import transaction
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from recommendation_list.filters import CustomRecommendationListFieldsFilter
from recommendation_list.models.recommendations import RecommendationList, Favorites, CategoryEnum, Recommendation
from recommendation_list.models.tags import Tag
from recommendation_list.permissions import IsOwnerOrReadOnly, IsOwnerOrReadOnlyRecommendation
from recommendation_list.serializers.recommendations_serializers import RecommendationListSerializer, \
    FavoritesCreateSerializer, RecommendationSerializer
from recommendation_list.serializers.tags_serializers import TagSerializer


class RecommendationListViewSet(ModelViewSet):
    queryset = RecommendationList.objects.all()
    serializer_class = RecommendationListSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filterset_class = CustomRecommendationListFieldsFilter

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user
        return super().create(request, *args, **kwargs)

    @action(methods=['GET'], detail=False)
    def categories(self, request):
        return Response([elem.value for elem in CategoryEnum])

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def favorites(self, request, pk=None):
        request.data['user'] = request.user.id
        request.data['recommendation_list'] = pk
        serializer = FavoritesCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RecommendationViewSet(ModelViewSet):
    serializer_class = RecommendationSerializer
    permission_classes = [IsOwnerOrReadOnlyRecommendation]

    def get_queryset(self):
        return Recommendation.objects.filter(recommendation_list_id=self.kwargs['recommendation_list_pk'])


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]


class FavoritesViewSet(ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesCreateSerializer
    permission_classes = [AllowAny]
