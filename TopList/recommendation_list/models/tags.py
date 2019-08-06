from django.db import models

from recommendation_list.models.recommendations import RecommendationList


class Tag(models.Model):
    tag_name = models.CharField(max_length=500, default='')


class TagList(models.Model):
    recommendation_list = models.ForeignKey(RecommendationList, on_delete=models.CASCADE, related_name='tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='recommendations')
