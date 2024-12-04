from django.db import models
from django.core.exceptions import ValidationError
from ..utils import get_file_type  # Import the function from utils.py

from django.core.exceptions import ValidationError

class File(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=10, choices=[('pdf', 'PDF'), ('image', 'Image')], blank=True)
    parsed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.file_type:
            file_type = get_file_type(self.file)
            if not file_type:
                raise ValidationError("Unsupported file type.")
            self.file_type = file_type
        super().save(*args, **kwargs)