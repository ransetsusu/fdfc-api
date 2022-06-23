
from atexit import register
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


REGISTER_URL = reverse('user-register')
GET_STARTED_URL = reverse('user-getstarted')
TOKEN_URL = reverse('auth-token')
AUTH_USER_DETAIL_URL = reverse('auth-me')

class UserAPITests(APITestCase):
    fixtures = ['data']

    def setUp(self) -> None:
        self.user_model = get_user_model()

    def test_user_cannot_register_with_no_data(self):
        """ Test user registration """
        data = {}
        response = self.client.post(REGISTER_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cant_register_with_taken_username(self):
        data = {'username': 'test111', 'password': 'testpass1111'}
        response = self.client.post(REGISTER_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_register(self):
        """ Test user registration """
        data = {'username': 'foo', 'password': '1234'}
        response = self.client.post(REGISTER_URL, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.user_model.objects.count(), 3)
        self.assertEqual(response.json().get('username'), 'foo')

    def test_user_get_started_no_authentication(self):
        """ Ensures User can't get started without auth """
        data = {'email': 'foo@bar.com'}
        response = self.client.patch(GET_STARTED_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_get_started_authenticated(self):
        """ Ensure User is Authenticated to Get Started """
        data = {'email': 'foo@bar.com'}
        test_user1 = self.user_model.objects.get(pk=1)
        self.client.force_authenticate(test_user1)
        response = self.client.patch(GET_STARTED_URL, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('email'), data['email'])

    def test_user_cant_login_with_invalid_credentials(self):
        """ Ensures user cant obtain token with invalid credentials """
        data = {'username': 'foobar', 'password': 'foobar123'}
        register_res = self.client.post(REGISTER_URL, data, format='json')
        self.assertEqual(register_res.status_code, status.HTTP_201_CREATED)
        login_res = self.client.post(TOKEN_URL, {**data, 'password': 'wrongpassword'})
        self.assertEqual(login_res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_login(self):
        """ Ensures user can obtain token with valid credentials """
        data = {'username': 'johndoe', 'password': 'johndoe123'}
        register_res = self.client.post(REGISTER_URL, data, format='json')
        self.assertEqual(register_res.status_code, status.HTTP_201_CREATED)

        login_res = self.client.post(TOKEN_URL, data)
        self.assertEqual(login_res.status_code, status.HTTP_200_OK)
        self.assertContains(login_res, 'token')

    def test_user_cant_get_detail_without_authentication(self):
        """ Ensures user cant get details without authentication """
        response = self.client.get(AUTH_USER_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_get_detail(self):
        """ Test authenticated user to get his/her detail """
        test_user2 = self.user_model.objects.get(pk=2)
        self.client.force_authenticate(test_user2)

        response = self.client.get(AUTH_USER_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'username')
