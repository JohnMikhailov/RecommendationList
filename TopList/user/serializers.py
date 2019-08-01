from rest_framework import serializers

from recommendation_list.models.recommendations import RecommendationList
from .models import CustomUser


class CustomUserSerializerCreate(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ('id',
                  'email',
                  'first_name',
                  'last_name', 'username', 'password',
                  'is_active',
                  'avatar')
        read_only_fields = ('id', 'refresh_token')
        extra_kwargs = {'username': {'required': True},
                        'first_name': {'required': True},
                        'last_name': {'required': True},
                        'email': {'required': True},
                        'avatar': {'required': False}}


class CustomUserSerializer(CustomUserSerializerCreate):
    # recommendation_lists = serializers.PrimaryKeyRelatedField(many=True, queryset=RecommendationList.objects.all())

    class Meta:
        model = CustomUser
        fields = CustomUserSerializerCreate.Meta.fields
        read_only_fields = CustomUserSerializerCreate.Meta.read_only_fields + ('email',)
        extra_kwargs = {'username': {'required': True},
                        'first_name': {'required': True},
                        'last_name': {'required': True},
                        'avatar': {'required': False}}
