from django.db import models

class User(models.Model):
    username = models.CharField(max_length=16, verbose_name='username', unique=True)
    firstname = models.CharField(max_length=40, verbose_name='firstname')
    lastname = models.CharField(max_length=40, verbose_name='lastname')
    password = models.CharField(max_length=16, verbose_name='password')
    avatar = models.ImageField(upload_to='avatars/',default='default/avatar.jpg')
    is_private = models.BooleanField(default=False)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    media = models.ImageField(upload_to='images/')
    date = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)


class Friend(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')


class FriendRequest(models.Model):
    request_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_sender')
    request_reciver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_reciver')


class Chat(models.Model):
    chat_user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_user1')
    chat_user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_user2')


class ChatContent(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
