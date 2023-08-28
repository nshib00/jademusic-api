from django.urls import path, include, re_path
from rest_framework.authtoken import views as authtoken_views

from musapi import views

urlpatterns = [
    path('api/v1/track/download/', views.TrackDownloadView().as_view()),
    path('api/v1/track/get/', views.TrackGetView().as_view()),
    path('api/v1/album/download/', views.AlbumDownloadView().as_view()),
    path('api/v1/album/get/', views.AlbumGetView().as_view()),
    path('api/v1/playlist/download/', views.PlaylistDownloadView().as_view()),
    path('api/v1/playlist/get/', views.PlaylistGetView().as_view()),
    path('api/v1/user/list/', views.ListUserView().as_view()),
    path('api/v1/user/detail/<int:pk>/', views.DetailUserView().as_view()),
    path('api/v1/user/register/', views.RegisterUserView().as_view()),
    path('api/v1/user/register/check/', views.CheckUserRegistrationView().as_view()),
    path('api/v1/user/create_token/', views.CreateUserTokenView().as_view()),
    path('api/v1/auth/', include('djoser.urls')),
    re_path('^auth/', include('djoser.urls.authtoken')),
]