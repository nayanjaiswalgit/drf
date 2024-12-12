# views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Statement
from ..serializers import StatementSerializer
from rest_framework.exceptions import NotFound
from django.db import IntegrityError


class StatementViewSet(viewsets.ModelViewSet):
    queryset = Statement.objects.all()
    serializer_class = StatementSerializer

    def get_queryset(self):
        """
        Optionally restrict the queryset by filtering.
        You can add query parameters here for optimization, like search, filtering, etc.
        """
        queryset = Statement.objects.all()
        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Handle POST request for creating a new statement
        """
        try:
            
            return super().create(request, *args, **kwargs)
        except IntegrityError as e:
            return Response({"detail": f"Integrity error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Handle PATCH request for updating a statement.
        This allows partial updates.
        """
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Handle DELETE request for deleting a statement.
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except NotFound:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """
        Handle bulk POST request to create multiple statements at once.
        """
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            statements = serializer.save()
            return Response(self.get_serializer(statements, many=True).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['patch'])
    def bulk_update(self, request):
        """
        Handle bulk PATCH request to update multiple statements.
        """
        updated_statements = []
        for item in request.data:
            statement = Statement.objects.filter(id=item.get('id')).first()
            if statement:
                serializer = StatementSerializer(statement, data=item, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    updated_statements.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": f"Statement with id {item.get('id')} not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(updated_statements, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'])
    def bulk_delete(self, request):
        """
        Handle bulk DELETE request to delete multiple statements.
        """
        ids_to_delete = request.data.get('ids', [])
        if not ids_to_delete:
            return Response({"detail": "No IDs provided"}, status=status.HTTP_400_BAD_REQUEST)

        statements_to_delete = Statement.objects.filter(id__in=ids_to_delete)
        deleted_count, _ = statements_to_delete.delete()
        if deleted_count > 0:
            return Response({"detail": f"{deleted_count} statements deleted."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "No statements found with the provided IDs."}, status=status.HTTP_404_NOT_FOUND)
