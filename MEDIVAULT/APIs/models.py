from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
import uuid as uuid_lib


class Individual(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False, unique=True)
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, unique=True)

    def __str__(self):
        return self.firstName + " " + self.lastName


class Organization(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, unique=True)

    def __str__(self):
        return self.name