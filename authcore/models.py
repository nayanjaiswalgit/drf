from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid





class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bio = models.CharField(max_length=255, blank=True)
    cover_photo = models.ImageField(upload_to='covers/', null=True, blank=True)

    def __str__(self):
        return self.username
    

class GoogleCredentials(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.TextField()
    token_uri = models.TextField()
    client_id = models.TextField()
    client_secret = models.TextField()
    scopes = models.TextField()
