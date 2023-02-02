from django.urls import path
from tweet.views import (IndexView, CallbackView)

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('twitter/callback/', CallbackView.as_view(), name='callback'),
]
