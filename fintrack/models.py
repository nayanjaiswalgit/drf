from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
import  uuid
from django.core.validators import MinValueValidator, MaxValueValidator

month_validators = [MinValueValidator(1), MaxValueValidator(12)] 
year_validators = [MinValueValidator(2020), MaxValueValidator(2050)]
# Base model with common validation
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True , editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


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


class Transaction(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="transactions")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    is_investment = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.account.username} paid {self.amount} for {self.group.name} ({'Investment' if self.is_investment else 'Expense'})"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Expense(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="expenses")
    item_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="expenses")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.item_name} - ${self.price} ({self.category.name})"


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
