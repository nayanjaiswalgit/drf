from google_auth_oauthlib.flow import Flow
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import GoogleCredentials

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, 'secrets', 'client_secret.json')

class GoogleLoginAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRET_FILE,
            scopes=['https://www.googleapis.com/auth/gmail.readonly'],
            redirect_uri='http://localhost:8000/api/oauth/callback'
        )
        auth_url, _ = flow.authorization_url(prompt='consent')
        return Response({"auth_url": auth_url})
    

class OAuthCallbackAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRET_FILE,
            scopes=['https://www.googleapis.com/auth/gmail.readonly'],
            redirect_uri='http://localhost:8000/api/oauth/callback'
        )
        flow.fetch_token(authorization_response=request.build_absolute_uri())

        credentials = flow.credentials

        # Save credentials to the database
        GoogleCredentials.objects.update_or_create(
            user=request.user,
            defaults={
                'access_token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': " ".join(credentials.scopes),
            }
        )

        return Response({"message": "Google account linked successfully."})
