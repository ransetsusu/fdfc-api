from dataclasses import fields
from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model() # auth.User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'id')


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data.get('password'))
        user.is_active = True
        user.save()

        return user


class UserGetStartedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'last_login', 'is_staff', 'is_active', 'date_joined',
        )
        extra_kwargs = {
            'is_staff': {'read_only': True},
            'is_active': {'read_only': True},
            'date_joined': {'read_only': True},
        }
