from django.db import models

# Create your models here.

class Subscribers(models.Model):
    username = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    chat_id = models.CharField(max_length=40)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.username+' - '+self.city