from django.db.models import F, Q
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from recommendation_list.filters import CustomUserFavoritesFilter
from recommendation_list.models.recommendations import Favorites
from recommendation_list.serializers.recommendations_serializers import FavoritesListSerializer, \
    RecommendationListSerializer
from user.models import CustomUser
from user.serializers import CustomUserSerializer
from user.permissions import IsOwnerOrReadOnly


class UserViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ['get', 'patch', 'head', 'options']
    filterset_class = [CustomUserFavoritesFilter]

    @action(methods=['GET'], detail=True, permission_classes=[IsAuthenticated])
    def favorites(self, request, pk=None):
        users = CustomUser.objects.all()
        searched_user = get_object_or_404(queryset=users, id=pk)
        queryset = searched_user.favorites.all()
        serializer = RecommendationListSerializer(queryset, many=True)
        return Response(serializer.data)
