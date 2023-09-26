from django.db import models

# Create your models here.
class Message(models.Model):
    user = models.CharField(max_length=50)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
