from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class AuthorizationSerializer(serializers.Serializer):

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
