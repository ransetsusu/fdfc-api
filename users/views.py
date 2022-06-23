from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from users.serializers import (
    UserRegistrationSerializer, UserGetStartedSerializer)


User = get_user_model() # auth.User

class UserRegisterApiView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]


class UserGetStartedApiView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserGetStartedSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.request.user.pk)
        self.check_object_permissions(self.request, obj)
        return obj


user_registration_view = UserRegisterApiView.as_view()
user_getting_started_view = UserGetStartedApiView.as_view()
