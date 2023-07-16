from django.urls import path

from . import organizationViews

urlpatterns = [
    path('signup/', organizationViews.signup, name='Signup'),
    path('login/', organizationViews.login, name='Login'),
    path('addFile/', organizationViews.add_file, name='Add File'),
    path('getFiles/', organizationViews.get_files, name='Get Files'),
    path('checkUser/', organizationViews.check_user, name='Check User'),
]
