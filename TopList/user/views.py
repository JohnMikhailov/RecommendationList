from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from TopList.custom_mixins.pagination import PaginationMixin
from recommendation_list.serializers.recommendations_serializers import RecommendationListSerializer
from user.models import CustomUser
from user.serializers import CustomUserSerializer
from user.permissions import IsOwnerOrReadOnly, IsOwnerIdOrMe


class UserViewSet(PaginationMixin, ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ['get', 'patch', 'head', 'options']

    @action(methods=['GET'], detail=True, permission_classes=[IsAuthenticated])
    def favorites(self, request, pk=None):
        users = CustomUser.objects.all()
        searched_user = get_object_or_404(queryset=users, id=pk)
        queryset = searched_user.favorites.all()

        ordering_field = request.query_params.get('order', '')
        if ordering_field in ('create', '-create'):
            order = '-' if ordering_field[0] == '-' else ''
            queryset = queryset.order_by(order+'favorites_recommendations__created')

        serializer = RecommendationListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        if self.kwargs['pk'] == 'me':
            self.kwargs['pk'] = request.user.id
        return super().retrieve(request, *args, **kwargs)

    @action(methods=['GET'], detail=True, permission_classes=[IsOwnerIdOrMe])
    def drafts(self, request, *args, **kwargs):
        if not(kwargs['pk'] == 'me' or kwargs['pk'].isdigit()):
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.kwargs['pk'] = request.user.id
        drafts = request.user.lists.filter(is_draft=True)
        page = self.paginate_queryset(drafts)
        serializer = RecommendationListSerializer(page, many=True) if page \
            else RecommendationListSerializer(drafts, many=True)
        return Response(serializer.data)
