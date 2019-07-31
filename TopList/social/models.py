from django.db import models
from user.models import CustomUser


class RecommendationList(models.Model):
    is_draft = models.BooleanField(default=False)

    photo = models.ImageField(null=True)

    category = models.CharField(max_length=500, default='')
    header = models.CharField(max_length=500, default='')


class Favorites(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recommendation_list = models.ForeignKey(RecommendationList, on_delete=models.CASCADE)


class Recommendation(models.Model):
    recommendation_list = models.ForeignKey(RecommendationList, on_delete=models.CASCADE)

    text = models.CharField(max_length=1000, default='')


class Tag(models.Model):
    tag_name = models.CharField(max_length=500, default='')


class TagList(models.Model):
    recommendation_list = models.ForeignKey(RecommendationList, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
