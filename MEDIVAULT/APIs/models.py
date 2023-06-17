from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

# Create your models here.


class Individual (models.Model):
    id = models.AutoField(primary_key=True)      # change this to uuid later
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=254 , unique=True)

    def __str__(self):
        return self.firstName + " " + self.lastName


class Organization (models.Model):
    id = models.AutoField(primary_key=True)      # change this to uuid later
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, unique=True)

    def __str__(self):
        return self.name



