from django.urls import path
from .views import ChannelView

urlpatterns = [
    path('api', ChannelView.as_view()),
]