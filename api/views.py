from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .serializers import *  
from .services import *

class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    
    def post(self, request):
        serializer =  self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)

            login(request, user)
            user_serializer = UserAccountSerializer(user)
            context = {
                "success": "user account successfully created", 
                "auth": {
                    "user": user_serializer.data,
                    "token": token.key
                }
            }
            return Response(context) 
        else:
            return Response({"errors": serializer.errors})

class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = authenticate(self.request, username=serializer.validated_data['username'], password=serializer.validated_data['password'])

            if user is not None:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)

                return Response({
                    "auth": {
                        "user": UserAccountSerializer(user).data,
                        "token": token.key
                    }
                })
            else:
                return Response({
                    'errors': {
                        'messages': ['Invalid credentials']
                    }
                })
        else:
            return Response({'errors': serializer.errors})

class LogoutView(generics.RetrieveAPIView):

    def get(self, request):
        if request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()

            logout(request)

        return Response({'success': 'User logged out successfully'})

class PostRecordsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PostService.get_all_posts()
    serializer_class = PostSerializer

    def list(self, request):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            for item in serializer.data:
                is_liked = {}
                is_liked['is_liked'] = PostService.is_post_liked(item['id'], request.user)
                item.update(is_liked)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class PostCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'user': request.user})

        if serializer.is_valid():
            post = serializer.save()

            context = {
                'success': 'Post was successfully created',
                'post': self.serializer_class(post).data
            }

            return Response(context)
        else:
            context = {
                'errors': serializer.errors,
            }

            return Response(context)

class PostEditView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def put(self, request, post_id):
        serializer = self.serializer_class(data=request.data, context={'user': request.user, 'post_id':post_id})

        if serializer.is_valid():
            result = serializer.edit_post()

            return Response(result)
        else:
            return Response({'errors': serializer.errors})
    
    def get(self, request, post_id):
        post = PostService.get_post(post_id)

        if post is not None:
            return Response(self.serializer_class(post).data)
        else:
            return Response({
                'errors': {
                    'messages': ['Post not found']
                }
            })

class PostLikeView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostLikeSerializer

    def put (self, request, post_id):
        serializer = self.serializer_class(data=request.data, context={'user': request.user, 'post_id':post_id})
    
        if serializer.is_valid():
            result = serializer.update_post_like()

            return Response(result)

        
