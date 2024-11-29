from rest_framework import serializers
from ..models import MonthlyBalance

class MonthlyBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyBalance
        fields = ['account', 'balance', 'month', 'year']
