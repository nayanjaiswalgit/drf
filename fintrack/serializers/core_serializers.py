from rest_framework import serializers
from ..models import Income, Account, MonthlyBalance, Group, GroupMembership, Transaction, Expense, Category, ExpenseSplit, Balance
from authcore.models import CustomUser
from datetime import datetime

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id', 'income_source', 'income_amount', 'date_received']


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'account_number',]


class MonthlyBalanceSerializer(serializers.ModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = MonthlyBalance
        fields = ['id', 'account', 'balance', 'month', 'year']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'created_at']


class GroupMembershipSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    user = serializers.StringRelatedField()  # Assuming you want to display the username

    class Meta:
        model = GroupMembership
        fields = ['id', 'joined_at']


class TransactionSerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    expenses = serializers.PrimaryKeyRelatedField(queryset=Expense.objects.all(), many=True, required=False)

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'account', 'amount', 'is_credit', 'date', 'description', 'expenses']
        read_only_fields = ['user']  # User is automatically set

    def create(self, validated_data):
        # Get the user from the request context (automatically set)
        user = self.context['request'].user
        validated_data['user'] = user
        
        # Extract the date from the request data
        date = self.context['request'].data.get('date', None)

        
        # If date is provided in the request, use it, otherwise, set the default date
        if date:
            validated_data['date'] = date
        else:
            # Raise error if date is not provided
            raise serializers.ValidationError("Date is required.")


        # Create and return the instance
        return super().create(validated_data)


class ExpenseSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, required=False)
    category = serializers.StringRelatedField()

    class Meta:
        model = Expense
        fields = ['id', 'transactions', 'item_name', 'category', 'description', 'amount', 'date']
        read_only_fields = ['user']  # Make sure user is read-only as it will be set in the viewset
        
        
        
class ExpenseSplitSerializer(serializers.ModelSerializer):
    expense = ExpenseSerializer()
    user = serializers.StringRelatedField()

    class Meta:
        model = ExpenseSplit
        fields = ['id', 'expense', 'share']


class BalanceSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Assuming you want the username
    group = GroupSerializer()

    class Meta:
        model = Balance
        fields = ['id', 'group', 'balance']
