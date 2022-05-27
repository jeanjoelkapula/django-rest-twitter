from rest_framework import serializers
from django.contrib.auth import authenticate, login
from .models import * 
from .services import *

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
    

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
        read_only_fields = ['username', 'email']
        depth = 1

class PostSerializer(serializers.ModelSerializer):
    user = UserAccountSerializer(read_only=True)
    date_created = serializers.DateTimeField(format="%b.%d.%Y, %H:%M %p", read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['date_created']
        depth = 1
    
    def save(self):
        post, created = PostService.create_post(user=self.context['user'], post=self.validated_data['post'])
        return post
    
    def edit_post(self):
        result = PostService.edit_post(user=self.context['user'], post_id=self.context['post_id'], content=self.validated_data['post'])
        
        return result
        
class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['is_like']

    
    def update_post_like(self):
        print(self.validated_data)
        result = PostService.update_post_like(user=self.context['user'], post_id=self.context['post_id'], liked=self.validated_data['is_like'])

        return result
        
    