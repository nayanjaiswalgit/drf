from django.db import models
from django.conf import settings



from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
import  uuid

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True , editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class TaskStatus(models.Model):
    TASK_TYPES = [
        ('STATEMENT_PARSING', 'Statement Parsing'),
        ('MAIL_PARSING', 'Mail Parsing'),
        ('SMS_PARSING', 'SMS Parsing'),
    ]

    TASK_STAGES = [
        ('PARSER', 'Parser'),
        ('AI', 'AI Parsing'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    ]

    task_type = models.CharField(max_length=50, choices=TASK_TYPES)
    task_stage = models.CharField(max_length=50, choices=TASK_STAGES, default='PARSER')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='PENDING')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')
    error_message = models.TextField(blank=True, null=True)
    additional_info = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    data = models.JSONField(null=True, blank=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task_type} ({self.task_stage}) - {self.status}"

    class Meta:
        ordering = ['-updated_at']


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
