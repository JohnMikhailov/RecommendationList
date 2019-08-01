from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from user.models import CustomUser
from user.serializers import CustomUserSerializer
from user.permissions import IsOwnerOrReadOnly


class UserViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ['get', 'patch', 'head', 'options']
