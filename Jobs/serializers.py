from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework import serializers

class Upload_Resume_Serializer(ModelSerializer):
    class Meta:
        model = Upload_Resume
        fields = '__all__'