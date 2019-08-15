from django.db import models

from recommendation_list.models.tags import Tag

from enum import Enum
from django_enum_choices.fields import EnumChoiceField

from user.models import CustomUser


class CategoryEnum(Enum):
    MOVIES = 'movies'
    BOOKS = 'books'
    RELAX = 'relax'
    KNOWLEDGE = 'knowledge'
    MUSIC = 'music'
    GAMES = 'games'
    FREE = 'free theme'


class RecommendationList(models.Model):

    user = models.ForeignKey(CustomUser, related_name='lists', on_delete=models.CASCADE, null=False)

    is_draft = models.BooleanField(default=False)

    photo = models.ImageField(upload_to='recommendation_list_images', null=True)

    category = EnumChoiceField(CategoryEnum)
    header = models.CharField(max_length=500, default='')
    description = models.CharField(max_length=200, default='')
    title = models.CharField(max_length=200, default='')
    tags = models.ManyToManyField(Tag)

    users = models.ManyToManyField(CustomUser, through='Favorites', related_name='favorites')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Favorites(models.Model):
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             related_name='favorites_user')

    recommendation_list = models.ForeignKey(RecommendationList,
                                            on_delete=models.CASCADE,
                                            related_name='favorites_recommendations')

    created = models.DateTimeField(auto_now_add=True)


class Recommendation(models.Model):
    recommendation_list = models.ForeignKey(RecommendationList,
                                            related_name='recommendations',
                                            on_delete=models.CASCADE)

    text = models.CharField(max_length=1000, default='')

    photo = models.ImageField(upload_to='recommendation_images', null=True)
