from django.db import models

class Message(models.Model):
    session_id = models.CharField(max_length=40)
    body = models.TextField(max_length=500)

    class Meta:
        ordering = ['-id']