from django.urls import path
from .views import UserRegistration, PostView, CreatePostView, ListPostView, PostLikeView, LoginUserView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
path('user_registration/',UserRegistration.as_view(), name='create_user'),
path('user_login/',LoginUserView.as_view(), name='login_user'),
path('create_post/',CreatePostView.as_view(), name='create_post'),
path('post/<int:pk>/',PostView.as_view(), name='post'),
path('posts/',ListPostView.as_view(), name='list_post'),
path('post_like/',PostLikeView.as_view(), name='post_like')

]
