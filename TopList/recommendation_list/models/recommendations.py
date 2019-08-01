from django.db import models
from user.models import CustomUser


class RecommendationList(models.Model):
    user = models.ForeignKey(CustomUser, related_name='lists', on_delete=models.CASCADE, null=True)

    is_draft = models.BooleanField(default=False)

    photo = models.ImageField(null=True)

    category = models.CharField(max_length=500, default='')
    header = models.CharField(max_length=500, default='')


class Favorites(models.Model):
    user = models.ForeignKey(CustomUser, related_name='favorites', on_delete=models.CASCADE)
    recommendation_list = models.ForeignKey(RecommendationList, on_delete=models.CASCADE)


class Recommendation(models.Model):
    recommendation_list = models.ForeignKey(RecommendationList,
                                            related_name='recommendations',
                                            on_delete=models.CASCADE)

    text = models.CharField(max_length=1000, default='')
