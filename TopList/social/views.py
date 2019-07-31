from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from social.models import RecommendationList
from social.serializers import RecommendationLstSerializer


class RecommendationListViewSet(ModelViewSet):
    queryset = RecommendationList.objects.all()
    serializer_class = RecommendationLstSerializer
    http_method_names = ['get', 'patch', 'post', 'put']
    # permission_classes = [AllowAny]
