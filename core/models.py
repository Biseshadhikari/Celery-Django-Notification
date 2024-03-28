from django.db import models
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# Create your models here.
class Creator(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE,null = True,blank = True)
    name = models.CharField(max_length=100)
    subscribers = models.ManyToManyField(User, related_name='publishers')

    def __str__(self):
        return self.name
    
    


class Notification(models.Model): 
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    title = models.CharField(max_length =200)
    is_seen = models.BooleanField(default = False)


class Post(models.Model): 
    creator = models.ForeignKey(Creator,on_delete = models.CASCADE)
    title = models.CharField(max_length = 200 )
    desc = models.TextField()

