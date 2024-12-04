from rest_framework import serializers
from ..models.parsing import ParsingRule

class ParsingRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParsingRule
        fields = '__all__'
