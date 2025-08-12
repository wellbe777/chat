from django.db import models

class Channel(models.Model):
    chat_name = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255)

class Message(models.Model):
    chat_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.TimeField(auto_now_add=True)