
# urls.py
from django.urls import path, include
from rest_framework.authtoken import views as rest_framework_views
from rest_framework.routers import DefaultRouter
from .views import IncomeViewSet, AccountViewSet, MonthlyBalanceViewSet, GroupViewSet, GroupMembershipViewSet, TransactionViewSet, ExpenseViewSet, ExpenseSplitViewSet, BalanceViewSet, MonthlyExpenseView, StatementViewSet
router = DefaultRouter()
router.register(r'incomes', IncomeViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'monthly_balances', MonthlyBalanceViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'group_memberships', GroupMembershipViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'expense_splits', ExpenseSplitViewSet)
router.register(r'balances', BalanceViewSet)
router.register(r'statements', StatementViewSet)
from .views.email_views import ReadEmailsAPIView
urlpatterns = [
    path('', include(router.urls)),
    path('monthly-expense/', MonthlyExpenseView.as_view(), name='monthly-expense'),
    path('api/read-emails/', ReadEmailsAPIView.as_view(), name='read_emails'),
        # path('process-ai/', AIProcessingView.as_view(), name='process-ai'),


]
