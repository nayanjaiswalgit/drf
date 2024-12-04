from rest_framework.views import APIView
from rest_framework.response import Response

class TransactionListView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"message": "Transaction list placeholder"})
