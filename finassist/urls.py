# urls.py

from django.urls import path
from .views import AIProcessingView, ParsingRuleView, BankStatementParserView
urlpatterns = [
    path('process-ai/', AIProcessingView.as_view(), name='process-ai'),
    path('parsing-rules/', ParsingRuleView.as_view(), name='parsing_rules'),
    path('parse-bank-statement/', BankStatementParserView.as_view(), name='parse_bank_statement'),
]
