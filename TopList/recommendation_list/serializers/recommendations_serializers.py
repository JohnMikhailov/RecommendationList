from rest_framework import serializers

from recommendation_list.models.recommendations import RecommendationList, Favorites, Recommendation, CategoryEnum
from recommendation_list.models.tags import Tag
from recommendation_list.serializers.tags_serializers import TagSerializer
from user.serializers import CustomUserSerializer
from django_enum_choices.serializers import EnumChoiceField


class RecommendationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recommendation
        fields = ['text', 'photo']


class RelatedCustomUserField(CustomUserSerializer):
    def to_internal_value(self, data):
        return data


class RecommendationListSerializer(serializers.ModelSerializer):
    recommendations = RecommendationSerializer(many=True, required=True)
    user = RelatedCustomUserField()
    category = EnumChoiceField(CategoryEnum)
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = RecommendationList
        fields = ['id', 'recommendations', 'tags', 'user', 'is_draft', 'photo', 'category', 'header']
        extra_kwargs = {
            'tags': {'required': False}
        }

    def create(self, validated_data):
        recommendations = validated_data.pop('recommendations')
        recommendation_list = super().create(validated_data)
        for recommendation in recommendations:
            Recommendation.objects.create(recommendation_list=recommendation_list, **recommendation)

        tags = validated_data.get('tags', [])
        for tag in tags:
            new_tag, created = Tag.objects.get_or_create(tag_name=tag['tag_name'])
            recommendation_list.tags.add(new_tag)
        return recommendation_list


class FavoritesSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(many=True)
    recommendation_list = RecommendationListSerializer(many=True)

    class Meta:
        model = Favorites
        fields = '__all__'
