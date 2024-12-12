from rest_framework import serializers
from ..models.base_models import MonthlyBalance

class MonthlyBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyBalance
        fields = ['account', 'balance', 'month', 'year']
