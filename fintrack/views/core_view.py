
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Income, Account, MonthlyBalance, Group, GroupMembership, Transaction, Expense, ExpenseSplit, Balance
from ..serializers import IncomeSerializer, AccountSerializer, MonthlyBalanceSerializer, GroupSerializer, GroupMembershipSerializer, TransactionSerializer, ExpenseSerializer, ExpenseSplitSerializer, BalanceSerializer

# Income API
class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view

# Account API
class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view

# Monthly Balance API
class MonthlyBalanceViewSet(viewsets.ModelViewSet):
    queryset = MonthlyBalance.objects.all()
    serializer_class = MonthlyBalanceSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view

# Group API
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view

# Group Membership API
class GroupMembershipViewSet(viewsets.ModelViewSet):
    queryset = GroupMembership.objects.all()
    serializer_class = GroupMembershipSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view

# Transaction API
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view

# Expense API
class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view

# Expense Split API
class ExpenseSplitViewSet(viewsets.ModelViewSet):
    queryset = ExpenseSplit.objects.all()
    serializer_class = ExpenseSplitSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view

# Balance API
class BalanceViewSet(viewsets.ModelViewSet):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view
