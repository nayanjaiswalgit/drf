from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid





class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bio = models.CharField(max_length=255, blank=True)
    cover_photo = models.ImageField(upload_to='covers/', null=True, blank=True)

    def __str__(self):
        return self.username
    


