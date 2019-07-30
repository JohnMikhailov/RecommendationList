from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from user.models import CustomUser
from user.serializers import CustomUserSerializer
from user.permissions import IsOwnerOrReadOnly


class UserViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    http_method_names = ['get', 'patch', 'head', 'options']
