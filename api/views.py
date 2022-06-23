from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import generics, views

from users.serializers import UserSerializer


User = get_user_model()

class RootApiView(views.APIView):
    permission_classes = []

    def get(self, request, format=None):
        return Response({'message': 'FDFC exam API'})


class AuthUserApiView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.request.user.pk)
        self.check_object_permissions(self.request, obj)
        return obj


index_view = RootApiView.as_view()
auth_me_api_view = AuthUserApiView.as_view()
