from rest_framework import serializers

from recommendation_list.models.recommendations import RecommendationList, Favorites, Recommendation, CategoryEnum
from user.serializers import CustomUserSerializer
from django_enum_choices.serializers import EnumChoiceField


class RecommendationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recommendation
        fields = ['text', 'recommendation_list']
        extra_kwargs = {'recommendation_list': {'required': False}}


class RelatedCustomUserField(CustomUserSerializer):
    def to_internal_value(self, data):
        return data


class RecommendationListSerializer(serializers.ModelSerializer):
    recommendations = RecommendationSerializer(many=True)
    user = RelatedCustomUserField()
    category = EnumChoiceField(CategoryEnum)

    class Meta:
        model = RecommendationList
        fields = ['recommendations', 'user', 'is_draft', 'photo', 'category', 'header']

    def create(self, validated_data):
        recommendations = validated_data.pop('recommendations')
        recommendation_list = super().create(validated_data)
        for recommendation in recommendations:
            Recommendation.objects.create(recommendation_list=recommendation_list, **recommendation)
        return recommendation_list


class FavoritesSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(many=True)
    recommendation_list = RecommendationListSerializer(many=True)

    class Meta:
        model = Favorites
        fields = '__all__'
