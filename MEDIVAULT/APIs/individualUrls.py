from django.urls import path

from . import individualViews

urlpatterns = [
    path('signup/', individualViews.signup, name='Signup'),
    path('login/', individualViews.login, name='Login'),
    path('refreshToken/', individualViews.refresh_access_token, name='User'),
    path('isAuthenticated/', individualViews.is_authenticated, name='Is Authenticated'),
]