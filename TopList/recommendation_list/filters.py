import django_filters
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
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

    search = django_filters.CharFilter(method='common_filter')

    def common_filter(self, queryset, name, value):
        return queryset.filter(Q(header__icontains=value)
                               | Q(title__icontains=value)
                               | Q(description__icontains=value)
                               | Q(recommendations__text__icontains=value))

    order = django_filters.OrderingFilter(
        fields=(
            ('updated', 'updated')
        )
    )

    class Meta:
        model = RecommendationList
        fields = ['category', 'user_id', 'header', 'title', 'description', 'tags', 'updated']
