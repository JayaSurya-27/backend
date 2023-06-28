from django.contrib import admin
from .models import Individual, Organization, Files

# Register your models here.

admin.site.register(Individual)
admin.site.register(Organization)
admin.site.register(Files)

