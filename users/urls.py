from django.urls import path

from users.views import user_registration_view, user_getting_started_view

urlpatterns = [
    path('register/', user_registration_view, name='user-register'),
    path('get-started/', user_getting_started_view, name='user-getstarted')
]
