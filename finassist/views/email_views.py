from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from authcore.models import GoogleCredentials
import base64
import logging
from ..models.emails import Email

# Setting up logging
logger = logging.getLogger(__name__)

class ReadEmailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_email_body(self, msg):
        """Fetch the email body, checking both plain text and HTML formats."""
        body = None
        if 'parts' in msg['payload']:
            for part in msg['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    break
                elif part['mimeType'] == 'text/html':
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    break
        else:
            body = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8')
        return body

    def get(self, request):
        try:
            # Fetch credentials for the logged-in user
            creds_obj = GoogleCredentials.objects.get(user=request.user)
        except GoogleCredentials.DoesNotExist:
            return Response({"error": "Google account not linked."}, status=400)

        creds = Credentials(
            token=creds_obj.access_token,
            refresh_token=creds_obj.refresh_token,
            token_uri=creds_obj.token_uri,
            client_id=creds_obj.client_id,
            client_secret=creds_obj.client_secret,
            scopes=creds_obj.scopes.split(),
        )

        # Initialize the Gmail API client
        service = build('gmail', 'v1', credentials=creds)

        try:
            # Get the last processed email's ID
            last_processed_email = Email.objects.filter(user=request.user).order_by('-date').first()
            query = ""
            if last_processed_email:
                query = f"after:{last_processed_email.date.isoformat()}"

            # Fetch emails, handle pagination if necessary
            results = service.users().messages().list(userId='me', maxResults=50, q=query).execute()
            messages = results.get('messages', [])

            # If no new emails, return a message
            if not messages:
                return Response({"message": "No new emails."}, status=200)

            # Initialize list to store emails' data
            emails_data = []

            # Process each message
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()

                # Extract email details
                from_email = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'From'), None)
                subject = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'Subject'), None)
                date = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'Date'), None)
                email_body = self.get_email_body(msg)

                # Save email to the database
                email = Email.objects.create(
                    user=request.user,
                    message_id=message['id'],
                    from_email=from_email,
                    subject=subject,
                    date=date,
                    email_body=email_body
                )

                emails_data.append({
                    "from_email": from_email,
                    "subject": subject,
                    "date": date,
                    "email_body": email_body,
                })

            return Response(emails_data, status=200)

        except Exception as error:
            logger.error(f"Error occurred while fetching emails: {str(error)}")
            return Response({"error": f"An error occurred: {str(error)}"}, status=500)
