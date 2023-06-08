from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('login', views.login, name='login'),
    path('signout', views.signout, name='signout'),
    path('register', views.register, name='register'),
    path('users', views.profile, name='profile'),
    path('users/<slug:username>/', views.profile, name='profile'),
    path('newpost', views.newpost, name='newpost'),
    path('request/<slug:username>/', views.sendRequest, name='addfriend'),
    path('friends', views.friends, name='friends'),
    path('friends/<slug:username>/<slug:method>', views.friendsCtrl, name='fr_ctrl'),
    path('alusers',views.allUsers, name='allusers'),
]