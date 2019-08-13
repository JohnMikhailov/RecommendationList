import django_filters
from django_enum_choices.filters import EnumChoiceFilter

from recommendation_list.models.recommendations import CategoryEnum, RecommendationList
from recommendation_list.models.tags import Tag


class TagsFilter(django_filters.CharFilter):

    def filter(self, qs, value):
        if value:
            tags = [tag.strip() for tag in value.split(',')]
            qs = qs.filter(tags__name__in=tags)
        return qs


class CustomRecommendationListFieldsFilter(django_filters.FilterSet):
    category = EnumChoiceFilter(CategoryEnum)
    tags = TagsFilter(field_name='tags')

    class Meta:
        model = RecommendationList
        fields = ['category', 'user_id', 'is_draft', 'header', 'tags']
