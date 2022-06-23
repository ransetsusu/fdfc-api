from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from api.views import index_view, auth_me_api_view


urlpatterns = [
    path('', index_view),
    path('auth/login/', obtain_auth_token, name='auth-token'),
    path('auth/.me/', auth_me_api_view, name='auth-me'),
    path('users/', include('users.urls'))
]
