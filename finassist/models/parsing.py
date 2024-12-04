from django.db import models
from django.db.models import JSONField
from django.conf import settings
class ParsingRule(models.Model):
    bank_name = models.CharField(max_length=255, unique=True)
    file_type = models.CharField(max_length=50, choices=[('pdf', 'PDF'), ('csv', 'CSV'), ('txt', 'Text')])
    regex_pattern = models.TextField(null=True, blank=True)  # For PDFs and text files
    column_mapping = JSONField(null=True, blank=True)       # For CSV column mappings
    date_format = models.CharField(max_length=100, null=True, blank=True)  # Date format normalization
    description = models.TextField(null=True, blank=True)   # Optional notes about the rule
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bank_name} ({self.file_type})"



class processed_data(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data = JSONField(null=True, blank=True)