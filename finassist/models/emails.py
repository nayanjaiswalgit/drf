from django.db import models
from django.conf import settings

class Email(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="emails")
    message_id = models.CharField(max_length=255, unique=True)
    from_email = models.EmailField()
    subject = models.CharField(max_length=255)
    date = models.DateTimeField()
    email_body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.from_email}"
