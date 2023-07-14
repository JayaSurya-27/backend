from django.urls import path

from . import individualViews

urlpatterns = [
    path('signup/', individualViews.signup, name='Signup'),
    path('login/', individualViews.login, name='Login'),
    path('refreshToken/', individualViews.refresh_access_token, name='User'),
    path('isAuthenticated/', individualViews.is_authenticated, name='Is Authenticated'),
    path('addFile/', individualViews.add_file, name='Add File'),
    path('getFiles/', individualViews.get_files, name='Get Files'),
    path('downloadFile/<str:file_id>/', individualViews.download_file, name='Download File'),
    path('deleteFile/<str:file_id>/', individualViews.delete_file, name='Delete File'),
]