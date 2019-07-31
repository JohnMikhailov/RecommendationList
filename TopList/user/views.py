from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from user import serializers
from user.models import CustomUser
from user.serializers import CustomUserSerializer, CustomUserSerializerUpdate
from user.permissions import IsOwnerOrReadOnly


class UserViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = CustomUser.objects.all()
    http_method_names = ['get', 'patch', 'head', 'options']

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return CustomUserSerializerUpdate
        return CustomUserSerializer
