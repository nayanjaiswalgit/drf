from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.parsing import ParsingRule
from ..serializers.finassist_serializers import ParsingRuleSerializer

class ParsingRuleView(APIView):
    def get(self, request):
        """
        List all parsing rules or filter by bank_name.
        """
        bank_name = request.query_params.get('bank_name')
        if bank_name:
            rules = ParsingRule.objects.filter(bank_name__icontains=bank_name)
        else:
            rules = ParsingRule.objects.all()
        serializer = ParsingRuleSerializer(rules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new parsing rule.
        """
        serializer = ParsingRuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Update an existing parsing rule.
        """
        try:
            rule = ParsingRule.objects.get(pk=pk)
        except ParsingRule.DoesNotExist:
            return Response({"error": "Parsing rule not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ParsingRuleSerializer(rule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a parsing rule.
        """
        try:
            rule = ParsingRule.objects.get(pk=pk)
            rule.delete()
            return Response({"message": "Parsing rule deleted"}, status=status.HTTP_204_NO_CONTENT)
        except ParsingRule.DoesNotExist:
            return Response({"error": "Parsing rule not found"}, status=status.HTTP_404_NOT_FOUND)


from ..utils.file_parser import fetch_parsing_rule, parse_file
import os
import tempfile

class BankStatementParserView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        bank_name = request.data.get('bank_name')
        file_type = file.name.split('.')[-1]

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file_path = temp_file.name
            for chunk in file.chunks():
                temp_file.write(chunk)

        # Fetch parsing rule
        rule = fetch_parsing_rule(bank_name, file_type, ParsingRule)
        if not rule:
            return Response({"error": "No parsing rule found for the specified bank and file type."}, status=status.HTTP_404_NOT_FOUND)

        try:
            transactions = parse_file(file_path, rule)
            return Response({"transactions": transactions}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            # Clean up
            if os.path.exists(file_path):
                os.remove(file_path)
