from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authentication.utils import create_token
from user.models import CustomUser


class CustomUserTest(APITestCase):

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
        self.test_user_1.save()
        self.test_user_2.save()

    def test_user_can_change_own_data(self):
        user_id = self.test_user_1.id
        url = reverse('users-detail', kwargs={'pk': user_id})
        data = {
            'username': 'new_name',
            'password': 'new_password',
            'first_name': 'first_name',
            'last_name': 'last_name'
        }
        access_token = create_token({'id': user_id,
                                     'email': 'email@mail.com'}, 'access')
        self.client.credentials(HTTP_AUTHORIZATION='jwt ' + access_token)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_view_own_profile(self):
        user_id = self.test_user_1.id
        url = reverse('users-detail', kwargs={'pk': user_id})
        data = {
            'username': 'username1',
            'password': 'password',
            'email': 'email@mail.com',
            'first_name': 'first_name',
            'last_name': 'last_name'
        }
        access_token = create_token({'id': user_id,
                                     'email': 'email@mail.com'}, 'access')
        self.client.credentials(HTTP_AUTHORIZATION='jwt ' + access_token)
        response = self.client.get(url, data, format='json',)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anyone_can_view_any_profile(self):
        url = reverse('users-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_do_not_allow_to_user_add_new_user(self):
        url = reverse('users-list')
        data = {
            'username': 'username1',
            'password': 'password',
            'email': 'email@mail.com',
            'first_name': 'first_name',
            'last_name': 'last_name'
        }
        access_token = create_token({'id': self.test_user_1.id,
                                     'email': 'email@mail.com'}, 'access')
        self.client.credentials(HTTP_AUTHORIZATION='jwt ' + access_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_do_not_allow_to_user_delete_any_user(self):
        user_id = self.test_user_1.id
        url = reverse('users-detail', kwargs={'pk': user_id + 1})
        access_token = create_token({'id': user_id,
                                     'email': 'email@mail.com'}, 'access')
        self.client.credentials(HTTP_AUTHORIZATION='jwt ' + access_token)
        response = self.client.delete(url, foramt='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_do_not_allow_to_user_to_change_own_email(self):
        user_id = self.test_user_1.id
        url = reverse('users-detail', kwargs={'pk': user_id})
        access_token = create_token({'id': user_id,
                                     'email': 'email@mail.com'}, 'access')
        data = {
            'email': 'new_email'
        }
        self.client.credentials(HTTP_AUTHORIZATION='jwt ' + access_token)
        response = self.client.patch(url, data, foramt='json')
        self.assertEqual(self.test_user_1.email, response.data['email'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_change_own_avatar(self):
        user_id = self.test_user_1.id
        url = reverse('users-detail', kwargs={'pk': user_id})
        access_token = create_token({'id': user_id,
                                     'email': 'emial@mail.com'}, 'access')
        im = open('./test_media/avatars/im2.jpg', 'rb')
        data = {
            'avatar': im
        }
        self.client.credentials(HTTP_AUTHORIZATION='jwt ' + access_token)
        response = self.client.patch(url, data, foramt='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_trying_send_text_instead_of_image(self):
        user_id = self.test_user_1.id
        url = reverse('users-detail', kwargs={'pk': user_id})
        access_token = create_token({'id': user_id,
                                     'email': 'emial@mail.com'}, 'access')
        im = open('./test_media/avatars/false.rtf', 'rb')
        data = {
            'avatar': im
        }
        self.client.credentials(HTTP_AUTHORIZATION='jwt ' + access_token)
        response = self.client.patch(url, data, foramt='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
