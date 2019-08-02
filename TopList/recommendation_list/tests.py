from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authentication.utils import create_token
from user.models import CustomUser


class RecommendationListTest(APITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.test_user_1 = CustomUser.objects.create(username='username1',
                                                     password='password',
                                                     email='email@mail.com',
                                                     first_name='first_name',
                                                     last_name='last_name')
        self.test_user_1.save()

    def test_getting_category_list(self):
        url = reverse('categories')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_getting_list_of_all_recommendations(self):
        url = reverse('recommendation_list-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_creating_a_new_recommendation_list(self):
        user_id = self.test_user_1.id
        access_token = create_token({'id': user_id,
                                     'email': self.test_user_1.email}, 'access')
        url = reverse('recommendation_list-list')
        self.client.credentials(HTTP_AUTHORIZATION='jwt ' + access_token)
        data = {
            'recommendations': [
                {'text': 'test_text'}
            ],
            'is_draft': 'true',
            'category': 'Music',
            'header': 'header'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
