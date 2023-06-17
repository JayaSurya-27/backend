from django.urls import path, include

from . import individualUrls, organizationUrls

urlpatterns = [
    path('individual/', include(individualUrls)),
    path('organization/', include(organizationUrls)),
]
