from django.db import models
from django.conf import settings

class Email(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="emails")
    
    message_id = models.CharField(max_length=255, unique=True)
    
    snippet =  models.TextField(blank=True, null=True)
    
    from_email = models.EmailField(blank=True, null=True)
    
    from_email_name =  models.CharField(max_length=255, blank=True, null=True)
    
    subject = models.CharField(max_length=255)
    
    date = models.DateTimeField(blank=True, null=True)

    
    raw_html = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    raw_text = models.TextField(blank=True, null=True)

    label = models.CharField(max_length=50, blank=True, null=True)  # Optional field for labels (like spam/ham)

    processed_text = models.TextField(blank=True, null=True)  # This can store cleaned, tokenized, or vectorized content
    
    is_processed = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.subject} - {self.from_email}"
