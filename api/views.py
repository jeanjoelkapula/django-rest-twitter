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
                return Response({'errors': serializer.errors})
        else:
            return Response({'errors': serializer.errors})

class LogoutView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        request.user.auth_token.delete()

        logout(request)

        return Response({'success': 'User logged out successfully'})

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
            return Response({'error': 'Post not found'})
