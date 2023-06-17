from django.urls import path

from . import individualViews

urlpatterns = [
    path('signup/', individualViews.signup, name='Signup'),
    path('login/', individualViews.login, name='Login'),
    path('refreshToken/', individualViews.refresh_token, name='User'),
]