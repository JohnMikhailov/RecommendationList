from django.db import transaction
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from TopList.custom_mixins.pagination import PaginationMixin
from recommendation_list.filters import CustomRecommendationListFieldsFilter
from recommendation_list.models.recommendations import RecommendationList, CategoryEnum, Recommendation
from recommendation_list.permissions import IsOwnerOrReadOnly, IsOwnerOrReadOnlyRecommendation
from recommendation_list.serializers.recommendations_serializers import RecommendationListSerializer, \
    FavoritesCreateSerializer, RecommendationSerializer, LikesSerializer
from user.serializers import CustomUserSerializer


class RecommendationListViewSet(PaginationMixin, ModelViewSet):
    # queryset = RecommendationList.objects.filter(is_draft=False)
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

    @action(methods=['POST'], detail=True)
    def like(self, request, pk=None):
        request.data['user'] = request.user.id
        request.data['recommendation_list'] = pk
        serializer = LikesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True)
    def likes(self, request, pk=None):
        recommendation_list = self.queryset.get(id=pk)
        users = recommendation_list.likes.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)


class RecommendationViewSet(ModelViewSet):
    serializer_class = RecommendationSerializer
    permission_classes = [IsOwnerOrReadOnlyRecommendation]

    def get_queryset(self):
        return Recommendation.objects.filter(recommendation_list_id=self.kwargs['recommendation_list_pk'])
