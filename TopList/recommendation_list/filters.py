import django_filters
from django_enum_choices.filters import EnumChoiceFilter, EnumChoiceFilterSetMixin

from recommendation_list.models.recommendations import CategoryEnum, RecommendationList


def custom_choice_builder(choice):
    return choice.value.lower(), choice.value


class CategoryFilter(django_filters.FilterSet):
    category = EnumChoiceFilter(CategoryEnum, choice_builder=custom_choice_builder)

    class Meta:
        model = RecommendationList
        fields = ['category', 'user_id', 'is_draft', 'header']
