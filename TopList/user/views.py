from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from user.models import CustomUser
from user.serializers import CustomUserSerializer
from user.permissions import IsOwnerOrReadOnly


class UserViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ['get', 'patch', 'head', 'options']

    @action(methods=['GET'], detail=True, permission_classes=[IsAuthenticated])
    def favorites(self, request, pk=None):
        # TODO: ...
        pass
