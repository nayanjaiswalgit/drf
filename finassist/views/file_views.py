from rest_framework.views import APIView
from rest_framework.response import Response

class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        return Response({"message": "File upload placeholder"})
