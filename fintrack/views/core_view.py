
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Income, Account, MonthlyBalance, Group, GroupMembership, Transaction, Expense, ExpenseSplit, Balance
from ..serializers import IncomeSerializer, AccountSerializer, MonthlyBalanceSerializer, GroupSerializer, GroupMembershipSerializer, TransactionSerializer, ExpenseSerializer, ExpenseSplitSerializer, BalanceSerializer
from django.shortcuts import get_object_or_404

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
    
    def perform_create(self, serializer):
        # Extract the user from the request object
        user = self.request.user
        
        # First, create the Expense instance with the user context
        expense = serializer.save(user=user)

        # Check if an account is provided in the request data
        account_id = self.request.data.get('account', None)
        
        
        if account_id:
            # If account_id is provided, fetch the corresponding Account object
            account = get_object_or_404(Account, id=account_id)
            
            transaction_data = {
                'account': account,
                'amount': expense.amount,
                'description': expense.description,
                'date': expense.date,
                'is_credit': False,  # Adjust this based on your logic
                'user': user  # Set user from context
            }

            # Create the Transaction and associate it with the Expense
            transaction = Transaction.objects.create(**transaction_data)
            expense.transactions.add(transaction)  # Add the transaction to the expense

        return expense
    
    
    
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
