# views.py

from rest_framework.response import Response
from rest_framework.views import APIView
from ..ai.ai_service import AIService
from rest_framework import status

class AIProcessingView(APIView):
    def post(self, request, *args, **kwargs):
        input_text = request.data.get("input_text", "")
        input_type = request.data.get("input_type", "")
        input_file = request.data.get("input_file", "")
        
        if not input_text:
            return Response({"error": "No input text provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Instantiate the AI service
        ai_service = AIService(model_type="ollama")  # You can dynamically change model type here
        
        try:
            result = ai_service.process_request(input_text, input_type, input_file)
            return Response({"response": result}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
