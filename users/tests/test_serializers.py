from django.test import TestCase
from users.serializers import (
    UserRegistrationSerializer, UserGetStartedSerializer)


class TestUserSerializer(TestCase):

    def test_user_registration_serializer(self):
        request_data = {
            'username': 'aaaaaaaa',
            'password': 'passsssss'
        }

        serializer = UserRegistrationSerializer(data=request_data)
        self.assertEqual(serializer.is_valid(), True)

    def test_user_getstarted_serializer(self):
        request_data = {
            'email': 'testemail@test.local',
            'first_name': 'test_fname',
            'last_name': 'test_lname'
        }

        serializer = UserGetStartedSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        self.assertEqual(serializer.is_valid(), True)
