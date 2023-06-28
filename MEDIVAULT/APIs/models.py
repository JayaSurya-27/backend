from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
import uuid


class Individual(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, unique=True)

    def __str__(self):
        return self.firstName + " " + self.lastName


class Organization(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, unique=True)

    def __str__(self):
        return self.name


class Files(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='files/')
    owner = models.ForeignKey(Individual, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    # add uploaded by field
    tags = ArrayField(models.CharField(max_length=200), blank=True, null=True)

    def __str__(self):
        return self.name


