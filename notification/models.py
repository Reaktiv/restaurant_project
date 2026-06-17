from django.db import models
from account.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()



class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    is_Read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"








