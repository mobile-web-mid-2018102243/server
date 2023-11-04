from django.urls import path
from django.urls import include
from rest_framework import routers
from .views import SignupView
from .views import SigninView
from .views import GetPostListView
from .views import GetMyPostListView
from .views import SolvePost


urlpatterns = [
    path('sign-up/', SignupView.as_view(),name = 'sign-up'),
    path('sign-in/', SigninView.as_view(),name = 'sign-in'),
    path('posts/', GetPostListView.as_view(),name = 'post-list'),
    path('posts/my-post', GetMyPostListView.as_view(),name = 'post-my-list'),
    path('posts/<int:pk>', SolvePost.as_view(),name = 'post-detail'),
    path('posts/<int:pk>', SolvePost.as_view(),name = 'post-detial'),
    path('posts/<int:pk>', SolvePost.as_view(),name = 'post-detial'),
]