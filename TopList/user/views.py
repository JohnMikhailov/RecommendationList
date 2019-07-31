from rest_framework.viewsets import ModelViewSet

from user.models import CustomUser
from user.serializers import CustomUserSerializerUpdate
from user.permissions import IsOwnerOrReadOnly


class UserViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializerUpdate
    http_method_names = ['get', 'patch', 'head', 'options']
