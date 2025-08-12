from django.urls import path
from .consumers import ChatView

urlpatterns = [
    path('chat', ChatView.as_asgi()),
]