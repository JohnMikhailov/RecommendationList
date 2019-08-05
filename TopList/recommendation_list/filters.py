import django_filters
from django_enum_choices.filters import EnumChoiceFilter, EnumChoiceFilterSetMixin

from recommendation_list.models.recommendations import CategoryEnum, RecommendationList


from recommendation_list.models.tags import Tag


class CustomRecommendationListFieldsFilter(django_filters.FilterSet):
    category = EnumChoiceFilter(CategoryEnum)

    class Meta:
        model = RecommendationList
        fields = ['category', 'user_id', 'is_draft', 'header']
