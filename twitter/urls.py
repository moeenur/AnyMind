from django.urls import path
from twitter import views

urlpatterns = [
    path('hashtags/<hashtag>', views.HashtagTweet.as_view(), name='tw-hashtags'),
    path('users/<user>', views.UserTweet.as_view(), name='tw-users'),
]
