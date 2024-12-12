from rest_framework import serializers
from ..models import Statement
from .task_serializer import TaskStatusSerializer
class StatementSerializer(serializers.ModelSerializer):
    task_statuses = TaskStatusSerializer(many=True, read_only=True)  # Use the related field

    class Meta:
        model = Statement
        fields = ['id', 'file', 'start_date', 'end_date', 'account', 'task_statuses']
