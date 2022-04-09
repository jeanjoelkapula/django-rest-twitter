from rest_framework import serializers
from django.contrib.auth import authenticate, login
from .models import * 

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    

class UserAccountSerialier(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['username', 'email']
        depth = 1
