from rest_framework import serializers
from .models import *


class IndividualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Individual
        fields = '__all__'


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Individual
        fields = ['email', 'password']


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = '__all__'


class GetFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ['id', 'name', 'file', 'tags', 'date']


class FileRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileRequest
        fields = '__all__'


class GetFileRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileRequest
        fields = ['id', 'name', 'file', 'owner.firstName', 'owner.lastName', 'date', 'status']
        # fields = '__all__'
