import boto3
from django.db.models import Q
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from TopList import settings
from authentication.utils import create_token
from recommendation_list.filters import TagsFilter
from recommendation_list.models.recommendations import RecommendationList, CategoryEnum, Recommendation, Favorites
from recommendation_list.models.tags import Tag
from user.models import CustomUser

from unittest.mock import patch

from moto import mock_s3

class RecommendationListTest(APITestCase):

    def setUp(self) -> None:
        super().setUp()
        tag1 = Tag.objects.create(name='test_tag1')
        tag2 = Tag.objects.create(name='test_tag1')
        tag3 = Tag.objects.create(name='test_tag3')

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
                                                              text='recommendation_text1')
        self.recommendation_list_1.tags.add(tag1)

        self.recommendation_list_2 = RecommendationList.objects.create(user=self.test_user_1,
                                                                       is_draft=True,
                                                                       category=CategoryEnum.BOOKS,
                                                                       header='header')

        self.recommendation_2 = Recommendation.objects.create(recommendation_list=self.recommendation_list_2,
                                                              text='recommendation_text2')
        self.recommendation_list_2.tags.add(tag2)
        self.recommendation_list_2.tags.add(tag3)


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
        response = self.client.post(url, data=data, format='json')
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
        self.assertEqual(len(response.data['results']), RecommendationList.objects.filter(user_id=self.test_user_1.id).count())

        self.recommendation_list = RecommendationList.objects.create(user=self.test_user_1,
                                                                     is_draft=False,
                                                                     category=CategoryEnum.MUSIC,
                                                                     header='header')

        self.recommendation = Recommendation.objects.create(recommendation_list=self.recommendation_list,
                                                            text='text')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), RecommendationList.objects.count())

    def test_filtering_by_category_valid_category_name(self):
        url = reverse('recommendation_list-list')
        response = self.client.get(url, {'category': 'music'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), RecommendationList.objects.filter(category=CategoryEnum.MUSIC).count())

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

    @patch('django.core.files.storage.FileSystemStorage.save')
    def test_user_can_change_recommendation_list_photo(self, mock):
        user_id = self.test_user_1.id
        url = reverse('users-detail', kwargs={'pk': user_id})
        access_token = create_token({'id': user_id,
                                     'email': 'emial@mail.com'}, 'access')
        im = open('./media/recommendation_list_images/im2.jpg', 'rb')
        data = {
            'photo': im
        }
        self.client.credentials(HTTP_AUTHORIZATION='jwt ' + access_token)
        response = self.client.patch(url, data=data, foramt='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tags_adding_or_updating(self):
        user_id = self.test_user_1.id
        url = reverse('recommendation_list-detail', kwargs={'pk': self.recommendation_list_1.id})
        access_token = create_token({'id': user_id,
                                     'email': 'emial@mail.com'}, 'access')
        data = {
            'tags': [
                {'name': 'test1'},
                {'name': 'test2'}
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='jwt ' + access_token)
        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # @patch('django.core.files.storage.FileSystemStorage.save')
    # @mock_s3
    # @patch('storages.backends.s3boto3.S3Boto3Storage') ?
    def test_adding_photos_to_recommendations(self):
        # mock.return_value = 'im2.jpg'
        user_id = self.test_user_1.id
        url = reverse('recommendation_detailing-detail', kwargs={'recommendation_list_pk': self.recommendation_list_1.id,
                                                                 'pk': self.recommendation_1.id})
        access_token = create_token({'id': user_id,
                                     'email': 'emial@mail.com'}, 'access')
        im = open('./media/recommendation_list_images/im2.jpg', 'rb')
        data = {
            'photo': im
        }
        self.client.credentials(HTTP_AUTHORIZATION='jwt ' + access_token)
        response = self.client.patch(url, data=data, foramt='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filtering_by_searched_text(self):
        url = reverse('recommendation_list-list')
        text = 'text'
        response = self.client.get(url, {'search': text}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), RecommendationList.objects.filter(Q(header__icontains=text)
                                                                               | Q(title__icontains=text)
                                                                               | Q(description__icontains=text)
                                                                               | Q(recommendations__text__icontains=text)).count())

    def test_searching_by_tags(self):
        url = reverse('recommendation_list-list')
        response = self.client.get(url, {'tags': ['test_tag1']}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), TagsFilter().filter(RecommendationList.objects.all(), 'test_tag1').count())

    def test_searching_by_text_in_recommendations(self):
        url = reverse('recommendation_list-list')
        text = 'recommendation_text1'
        response = self.client.get(url, {'search': text}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), RecommendationList.objects.filter(recommendations__text__icontains=text).count())

    def test_adding_to_favorites(self):
        url = reverse('recommendation_list-favorites', kwargs={'pk': self.recommendation_list_1.id})
        count = Favorites.objects.all().count()
        access_token = create_token({'id': self.test_user_1.id,
                                     'email': 'emial@mail.com'}, 'access')
        self.client.credentials(HTTP_AUTHORIZATION='jwt ' + access_token)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count + 1, Favorites.objects.all().count())

    def test_adding_to_favorites_unauthorized(self):
        url = reverse('recommendation_list-favorites', kwargs={'pk': self.recommendation_list_1.id})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Favorites.objects.all().count(), 0)

    def test_adding_to_favorites_twice(self):
        url = reverse('recommendation_list-favorites', kwargs={'pk': self.recommendation_list_1.id})
        count = Favorites.objects.all().count()
        access_token = create_token({'id': self.test_user_1.id,
                                     'email': 'emial@mail.com'}, 'access')
        self.client.credentials(HTTP_AUTHORIZATION='jwt ' + access_token)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(count + 1, Favorites.objects.all().count())

    def test_like(self):
        url = reverse('recommendation_list-like', kwargs={'pk': self.recommendation_list_1.id})
        count = self.recommendation_list_1.likes.count()
        access_token = create_token({'id': self.test_user_1.id,
                                     'email': 'emial@mail.com'}, 'access')
        self.client.credentials(HTTP_AUTHORIZATION='jwt ' + access_token)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count + 1, self.recommendation_list_1.likes.count())

    def test_like_unauthorized(self):
        url = reverse('recommendation_list-like', kwargs={'pk': self.recommendation_list_1.id})
        count = self.recommendation_list_1.likes.count()
        access_token = create_token({'id': self.test_user_1.id,
                                     'email': 'emial@mail.com'}, 'access')
        self.client.credentials(HTTP_AUTHORIZATION='jwt ' + access_token)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count + 1, self.recommendation_list_1.likes.count())

    def test_like_twice(self):
        url = reverse('recommendation_list-like', kwargs={'pk': self.recommendation_list_1.id})
        access_token = create_token({'id': self.test_user_1.id,
                                     'email': 'emial@mail.com'}, 'access')
        self.client.credentials(HTTP_AUTHORIZATION='jwt ' + access_token)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(1, self.recommendation_list_1.likes.count())

    def test_get_user_profile_me(self):
        url = reverse('users-detail', kwargs={'pk': 'me'})
        access_token = create_token({'id': self.test_user_1.id,
                                     'email': 'emial@mail.com'}, 'access')
        self.client.credentials(HTTP_AUTHORIZATION='jwt ' + access_token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.test_user_1.id)

    def test_get_drafts_me(self):
        url = reverse('users-drafts', kwargs={'pk': 'me'})
        access_token = create_token({'id': self.test_user_1.id,
                                     'email': 'emial@mail.com'}, 'access')
        self.client.credentials(HTTP_AUTHORIZATION='jwt ' + access_token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.test_user_1.lists.filter(is_draft=True).count())

    def test_sorting_by_adding_to_favorites_date_asc(self):
        url = reverse('users-favorites', kwargs={'pk': self.test_user_2.id})
        access_token = create_token({'id': self.test_user_1.id,
                                     'email': 'emial@mail.com'}, 'access')
        self.client.credentials(HTTP_AUTHORIZATION='jwt ' + access_token)
        Favorites.objects.create(user_id=self.test_user_2.id,
                                 recommendation_list_id=self.recommendation_list_1.id)
        Favorites.objects.create(user_id=self.test_user_2.id,
                                 recommendation_list_id=self.recommendation_list_2.id)
        response = self.client.get(url, {'order': 'create'}, format='json')
        ordered_by_date = [i['id'] for i in response.data]
        expected_order = [self.recommendation_list_1.id, self.recommendation_list_2.id]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ordered_by_date, expected_order)

    def test_sorting_by_adding_to_favorites_date_desc(self):
        url = reverse('users-favorites', kwargs={'pk': self.test_user_2.id})
        access_token = create_token({'id': self.test_user_1.id,
                                     'email': 'emial@mail.com'}, 'access')
        self.client.credentials(HTTP_AUTHORIZATION='jwt ' + access_token)
        Favorites.objects.create(user_id=self.test_user_2.id,
                                 recommendation_list_id=self.recommendation_list_1.id)
        Favorites.objects.create(user_id=self.test_user_2.id,
                                 recommendation_list_id=self.recommendation_list_2.id)
        response = self.client.get(url, {'order': '-create'}, format='json')
        ordered_by_date = [i['id'] for i in response.data]
        expected_order = [self.recommendation_list_2.id, self.recommendation_list_1.id]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ordered_by_date, expected_order)

    def test_soring_by_update_date_asc(self):
        url = reverse('recommendation_list-list')
        access_token = create_token({'id': self.test_user_1.id,
                                     'email': 'emial@mail.com'}, 'access')
        self.client.credentials(HTTP_AUTHORIZATION='jwt ' + access_token)
        response = self.client.get(url, {'order': 'updated'}, format='json')
        ordered_by_update = [i['id'] for i in response.data['results']]
        expected_order = [self.recommendation_list_1.id, self.recommendation_list_2.id]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ordered_by_update, expected_order)

    def test_soring_by_update_date_desc(self):
        url = reverse('recommendation_list-list')
        access_token = create_token({'id': self.test_user_1.id,
                                     'email': 'emial@mail.com'}, 'access')
        self.client.credentials(HTTP_AUTHORIZATION='jwt ' + access_token)
        response = self.client.get(url, {'order': '-updated'}, format='json')
        ordered_by_update = [i['id'] for i in response.data['results']]
        expected_order = [self.recommendation_list_2.id, self.recommendation_list_1.id]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ordered_by_update, expected_order)
