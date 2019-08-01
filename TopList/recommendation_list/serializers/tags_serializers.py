from rest_framework import serializers

from recommendation_list.models.tags import TagList, Tag
from recommendation_list.serializers.recommendations_serializers import RecommendationListSerializer


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class TagListSerializer(serializers.ModelSerializer):
    recommendation_list = RecommendationListSerializer(many=True)

    class Meta:
        model = TagList
        fields = '__all__'
