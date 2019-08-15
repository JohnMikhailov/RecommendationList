import django_filters
from django.contrib.postgres.aggregates import ArrayAgg
from django_enum_choices.filters import EnumChoiceFilter

from recommendation_list.models.recommendations import CategoryEnum, RecommendationList, Favorites


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
    header = django_filters.CharFilter(field_name='header', lookup_expr='icontains')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')

    order = django_filters.OrderingFilter(
        fields=(
            ('updated', 'update')
        )
    )

    class Meta:
        model = RecommendationList
        fields = ['category', 'user_id', 'is_draft', 'header', 'title', 'description', 'tags', 'updated']


class CustomUserFavoritesFilter(django_filters.FilterSet):

    o = django_filters.OrderingFilter(
        fields=(
            ('created', 'create')
        )
    )

    class Meta:
        model = RecommendationList
        fields = ['created']
