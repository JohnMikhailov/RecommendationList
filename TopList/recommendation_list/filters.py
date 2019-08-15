import django_filters
from django.contrib.postgres.aggregates import ArrayAgg
from django_enum_choices.filters import EnumChoiceFilter

from recommendation_list.models.recommendations import CategoryEnum, RecommendationList


class TagsFilter(django_filters.CharFilter):

    def filter(self, qs, value):
        if not value:
            return qs
        input_tags = [tag.strip() for tag in value.split(',')]
        qs = qs.annotate(tags_name=ArrayAgg('tags__name')).filter(tags_name__contains=input_tags)
        return qs


class CustomRecommendationListFieldsFilter(django_filters.FilterSet):
    category = EnumChoiceFilter(CategoryEnum)
    tags = TagsFilter(field_name='tags')

    class Meta:
        model = RecommendationList
        fields = ['category', 'user_id', 'is_draft', 'header', 'tags']
