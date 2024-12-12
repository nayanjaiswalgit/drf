from rest_framework import serializers
from ..models import TaskStatus


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields = ['id', 'task_type', 'task_stage', 'status', 'error_message', 'additional_info', 'created_at', 'updated_at', 'data']
