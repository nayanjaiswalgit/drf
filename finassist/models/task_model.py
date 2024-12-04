from django.db import models
from django.conf import settings
class Task(models.model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks")
    task_name = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    response = models.TextField(blank=True, null=True)
    task_json = models.JSONField(blank=True, null=True)