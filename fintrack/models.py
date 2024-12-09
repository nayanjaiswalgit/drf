from typing import Iterable
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
import  uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from time import timezone

month_validators = [MinValueValidator(1), MaxValueValidator(12)] 
year_validators = [MinValueValidator(2020), MaxValueValidator(2050)]
# Base model with common validation
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True , editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

class Counterparty(models.Model):
    """Model to represent the counterparty, either a User or an external entity."""
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    external_id = models.CharField(max_length=255, blank=True, null=True)

    # Generic foreign key to link to either a user or an external entity
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"Counterparty: {self.name}"



# Income Model
class Income(BaseModel):
    income_source = models.CharField(max_length=50)
    income_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_received = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="incomes", on_delete=models.CASCADE)


class Account(models.Model):
    account_name = models.CharField(max_length=100)
    limit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    account_number = models.CharField(max_length=20, unique=True)
    is_credit_card = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="accounts", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.account_name}"


# MonthlyBalance Model
class MonthlyBalance(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="monthly_balances", on_delete=models.CASCADE)
    account = models.ForeignKey(Account, related_name="monthly_balances", on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    month = models.IntegerField(validators=month_validators)
    year = models.IntegerField(validators=year_validators)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['account', 'month', 'year', 'user'], name='unique_account_month_year')
        ]

    def __str__(self):
        if self.account.is_credit_card:
            # Ensure balance and limit are not None, default to 0 if they are
            balance = self.balance if self.balance is not None else 0
            limit = self.account.limit if self.account.limit is not None else 0
            return f"{self.account.account_name} - {self.month}/{self.year}: {limit - balance}"
        else:
            # Just show balance if it's not a credit card
            balance = self.balance if self.balance is not None else 0
            return f"{self.account.account_name} - {self.month}/{self.year}: {balance}"



class Group(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class GroupMembership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships")
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} in {self.group.name}"




class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


from django.utils import timezone

class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name="transactions", blank=True, null=True)
    account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name="transactions", blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_credit = models.BooleanField(default=False)
    date = models.DateField()
    description = models.TextField()

    # Many-to-many relationship with Expense, change related_name to avoid conflict
    expenses = models.ManyToManyField('Expense', related_name='transaction_expenses', blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'group', 'date']),
            models.Index(fields=['date']),  # Adding an index on the date for faster querying.
        ]
        ordering = ['-date']  # Ensures that transactions are ordered by date in descending order by default.

    def __str__(self):
        return f"Transaction by {self.user} for {self.amount} on {self.date.strftime('%Y-%m-%d')}"

    def clean(self):
        """Ensure the amount is always positive"""
        if self.amount <= 0:
            raise ValidationError("Amount must be greater than zero.")

    def save(self, *args, **kwargs):
        self.clean()  # Validate the instance before saving
        super().save(*args, **kwargs)

    def add_expense(self, expense):
        """Helper method to add an expense to the transaction and vice versa"""
        self.expenses.add(expense)
        expense.transactions.add(self)

class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="expenses")
    item_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="expenses", blank=True, null=True)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)  # Automatically sets the current date when a new record is created
    

    # Many-to-many relationship with Transaction, change related_name to avoid conflict
    transactions = models.ManyToManyField('Transaction', related_name='expense_transactions', blank=True)

    class Meta:
        indexes = [models.Index(fields=['user', 'category'])]

    def __str__(self):
        return f"Expense for '{self.item_name}' by {self.user}, Amount: {self.amount}"

    def clean(self):
        """Ensure the amount is always positive and paid status consistency"""
        if self.amount <= 0:
            raise ValidationError("Amount must be greater than zero.")
            

    def save(self, *args, **kwargs):
        self.clean()  # Validate the instance before saving
        super().save(*args, **kwargs)

    def add_transaction(self, transaction):
        """Helper method to add a transaction to the expense and vice versa"""
        self.transactions.add(transaction)
        transaction.expenses.add(self)



class ExpenseSplit(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name="splits")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    share = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} owes ${self.share} for {self.expense.item_name}"


class Balance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="balances")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="balances")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s balance in {self.group.name}: ${self.balance}"


class Statement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="statements")    
    file = models.FileField(upload_to='statements/', null=True, blank=True)
    start_date = models.DateField()  
    end_date = models.DateField()    
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="statements")
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"Statement from {self.start_date} to {self.end_date} for {self.user.username}"

    class Meta:
        ordering = ['-end_date']  


class MoneyTransaction(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="money_transactions")
    is_lend = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    counterparty = models.ForeignKey(Counterparty, on_delete=models.CASCADE, related_name="money_transactions")
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        transaction_type = "Lent" if self.is_lend else "Borrowed"
        return f"{transaction_type} {self.amount} to/from {self.counterparty.name} on {self.date}"

    class Meta:
        indexes = [
            models.Index(fields=['transaction', 'counterparty', 'date']),
            models.Index(fields=['date']),
        ]
        ordering = ['-date']
