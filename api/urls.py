from django.urls import path
from .views import *

urlpatterns = [
    path('auth/register/', RegistrationView.as_view(), name="register"),
    path('auth/login/', LoginView.as_view(), name="login"),
    path('auth/logout/', LogoutView.as_view(), name="logout"),
    path('<str:username>/profile/', UserProfileView.as_view(), name="get_profile"),
    path('<str:username>/follow/', FollowUserView.as_view(), name="follow_user"),
    path('posts/', PostRecordsView.as_view(), name="get_posts"),
    path('<str:username>/posts/', UserPostRecordsView.as_view(), name="get_user_posts"),
    path('post/', PostCreateView.as_view(), name='create_post'),
    path('post/<int:post_id>', PostEditView.as_view(), name="edit_post"),
    path('post/<int:post_id>/like/', PostLikeView.as_view(), name="edit_post_like"),
    path('post/<int:post_id>/unlike/', PostUnLikeView.as_view(), name="unlike_post")
]