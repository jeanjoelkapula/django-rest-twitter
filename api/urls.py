from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegistrationView.as_view(), name="register"),
    path('api-auth/login/', LoginView.as_view(), name="login"),
    path('api-auth/logout/', LogoutView.as_view(), name="logout"),
    path('post/', PostCreateView.as_view(), name='create_post')
]