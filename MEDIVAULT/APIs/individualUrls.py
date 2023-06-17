from django.urls import path

from . import individualViews

urlpatterns = [
    path('signup/', individualViews.signup, name='Signup'),
    path('login/', individualViews.login, name='Login'),
    path('user/', individualViews.userView, name='User'),
]