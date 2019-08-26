from rest_framework import serializers

from recommendation_list.models.tags import Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['name']
