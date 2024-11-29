from rest_framework import serializers
from ..models import Income, Account, MonthlyBalance, Group, GroupMembership, Transaction, Expense, Category, ExpenseSplit, Balance

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id', 'income_source', 'income_amount', 'date_received']


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'account_number', 'account_type']


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
        fields = ['id', 'group', 'joined_at']


class TransactionSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    account = AccountSerializer()

    class Meta:
        model = Transaction
        fields = ['id', 'group', 'account', 'amount', 'date', 'description', 'is_investment']


class ExpenseSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer()
    category = serializers.StringRelatedField()  # Assuming you want to show category name

    class Meta:
        model = Expense
        fields = ['id', 'transaction', 'item_name', 'category', 'description', 'price']


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
