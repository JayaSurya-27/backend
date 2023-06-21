from django.urls import path

from . import organizationViews

urlpatterns = [
    path('signup/', organizationViews.signup, name='Signup'),
    path('login/', organizationViews.login, name='Login'),
]
