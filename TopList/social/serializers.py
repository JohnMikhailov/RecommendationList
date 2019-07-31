from user.serializers import CustomUserSerializer
from .models import *

from rest_framework import serializers


class RecommendationLstSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecommendationList
        fields = '__all__'


class FavoritesSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(many=True)
    recommendation_list = RecommendationLstSerializer(many=True)

    class Meta:
        model = Favorites
        fields = '__all__'


class RecommendationSerializer(serializers.ModelSerializer):
    recommendation_list = RecommendationLstSerializer(many=True)

    class Meta:
        model = Recommendation
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class TagListSerializer(serializers.ModelSerializer):
    recommendation_list = RecommendationLstSerializer(many=True)

    class Meta:
        model = TagList
        fields = '__all__'
