from rest_framework import serializers

from recommendation_list.models.recommendations import RecommendationList, Favorites, Recommendation
from user.serializers import CustomUserSerializer


class RecommendationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recommendation
        fields = ['text', 'recommendation_list']
        extra_kwargs = {'recommendation_list': {'required': False}}


class RecommendationListSerializer(serializers.ModelSerializer):
    recommendations = RecommendationSerializer(many=True)
    user = CustomUserSerializer(required=False)

    class Meta:
        model = RecommendationList
        fields = ['recommendations', 'user', 'is_draft', 'photo', 'category', 'header']

    def create(self, validated_data):
        recommendations = validated_data.pop('recommendations')
        recommendation_list = RecommendationList.objects.create(**validated_data)
        for recommendation in recommendations:
            Recommendation.objects.create(recommendation_list=recommendation_list, **recommendation)
        return recommendation_list


class FavoritesSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(many=True)
    recommendation_list = RecommendationListSerializer(many=True)

    class Meta:
        model = Favorites
        fields = '__all__'
