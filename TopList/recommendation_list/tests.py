from django.urls import reverse
from django_enum_choices.fields import EnumChoiceField
from rest_framework import status
from rest_framework.test import APITestCase

from authentication.utils import create_token
from recommendation_list.models.recommendations import RecommendationList, CategoryEnum, Recommendation
from user.models import CustomUser


class RecommendationListTest(APITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.test_user_1 = CustomUser.objects.create(username='username1',
                                                     password='password',
                                                     email='email@mail.com',
                                                     first_name='first_name',
                                                     last_name='last_name')

        self.test_user_2 = CustomUser.objects.create(username='username2',
                                                     password='password',
                                                     email='email@mail.com',
                                                     first_name='first_name',
                                                     last_name='last_name')

        self.recommendation_list_1 = RecommendationList.objects.create(user=self.test_user_1,
                                                                       is_draft=False,
                                                                       category=CategoryEnum.MUSIC,
                                                                       header='header')

        self.recommendation_1 = Recommendation.objects.create(recommendation_list=self.recommendation_list_1,
                                                              text='text')

        self.recommendation_list_2 = RecommendationList.objects.create(user=self.test_user_1,
                                                                       is_draft=False,
                                                                       category=CategoryEnum.BOOKS,
                                                                       header='header')

        self.recommendation_2 = Recommendation.objects.create(recommendation_list=self.recommendation_list_2,
                                                              text='text')

    def test_getting_category_list(self):
        url = reverse('recommendation_list-categories')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_getting_list_of_all_recommendations(self):
        url = reverse('recommendation_list-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_creating_a_new_recommendation_list_valid_info(self):
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
            'category': 'music',
            'header': 'header'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_creating_a_new_recommendation_list_invalid_category(self):
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
            'category': 'category',  # invalid category
            'header': 'header'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_creating_a_new_recommendation_list_with_no_recommendations(self):
        access_token = create_token({'id': self.test_user_1.id,
                                     'email': self.test_user_1.email}, 'access')
        url = reverse('recommendation_list-list')
        self.client.credentials(HTTP_AUTHORIZATION='jwt ' + access_token)
        data = {
            'is_draft': 'true',
            'category': 'music',
            'header': 'header'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filtering_by_user_id(self):
        url = reverse('recommendation_list-list')
        response = self.client.get(url, {'user_id': self.test_user_1.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), RecommendationList.objects.filter(user_id=self.test_user_1.id).count())

        self.recommendation_list = RecommendationList.objects.create(user=self.test_user_1,
                                                                     is_draft=False,
                                                                     category=CategoryEnum.MUSIC,
                                                                     header='header')

        self.recommendation = Recommendation.objects.create(recommendation_list=self.recommendation_list,
                                                            text='text')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), RecommendationList.objects.count())

    def test_filtering_by_category_valid_category_name(self):
        url = reverse('recommendation_list-list')
        response = self.client.get(url, {'category': 'music'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), RecommendationList.objects.filter(category=CategoryEnum.MUSIC).count())

    def test_filtering_by_category_invalid_category_name(self):
        url = reverse('recommendation_list-list')
        response = self.client.get(url, {'category': 'Music'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_updating_recommendation_list_info_unauthorized(self):
        url = reverse('recommendation_list-detail', kwargs={'pk': self.recommendation_list_1.id})
        data = {
            'is_draft': 'true'
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_updating_recommendation_list_info_authorized(self):
        url = reverse('recommendation_list-detail', kwargs={'pk': self.recommendation_list_1.id})
        data = {
            'is_draft': 'true'
        }
        access_token = create_token({'id': self.test_user_1.id,
                                     'email': 'emial@mail.com'}, 'access')
        self.client.credentials(HTTP_AUTHORIZATION='jwt ' + access_token)
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_trying_update_foreign_list(self):
        url = reverse('recommendation_list-detail', kwargs={'pk': self.recommendation_list_1.id})
        data = {
            'is_draft': 'true'
        }
        access_token = create_token({'id': self.test_user_2.id,
                                     'email': 'emial@mail.com'}, 'access')
        self.client.credentials(HTTP_AUTHORIZATION='jwt ' + access_token)
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_change_recommendation_list_photo(self):
        user_id = self.test_user_1.id
        url = reverse('users-detail', kwargs={'pk': user_id})
        access_token = create_token({'id': user_id,
                                     'email': 'emial@mail.com'}, 'access')
        im = open('./media/recommendation_list_images/im2.jpg', 'rb')
        data = {
            'photo': im
        }
        self.client.credentials(HTTP_AUTHORIZATION='jwt ' + access_token)
        response = self.client.patch(url, data, foramt='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
