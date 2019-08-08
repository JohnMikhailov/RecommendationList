import django_filters
from django_enum_choices.filters import EnumChoiceFilter

from recommendation_list.models.recommendations import CategoryEnum, RecommendationList


class CustomRecommendationListFieldsFilter(django_filters.FilterSet):
    category = EnumChoiceFilter(CategoryEnum)

    class Meta:
        model = RecommendationList
        fields = ['category', 'user_id', 'is_draft', 'header']
