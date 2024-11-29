from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import MonthlyBalance
from datetime import datetime
from django.db.models import Sum, F
from rest_framework.permissions import IsAuthenticated

class MonthlyExpenseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Get the current date
        today = datetime.today()
        current_year = today.year
        
        # Get the user from the request
        user = request.user
        
        # Get all the balances for the current year
        balances = MonthlyBalance.objects.filter(
            user=user,
            year=current_year
        ).values('month').annotate(total_balance=Sum('balance')).order_by('month')

        # Create a dictionary to hold the balances for all months
        monthly_data = {month: {'total_balance': 0, 'monthly_expense': 0} for month in range(1, 13)}

        # Populate the dictionary with actual data from the database
        for entry in balances:
            monthly_data[entry['month']]['total_balance'] = entry['total_balance']

        # Calculate monthly expenses
        previous_month_balance = 0
        for month in range(1, 13):
            current_month_balance = monthly_data[month]['total_balance']
            monthly_data[month]['monthly_expense'] = current_month_balance - previous_month_balance
            previous_month_balance = current_month_balance

        # Return the result as a response
        return Response(monthly_data)
