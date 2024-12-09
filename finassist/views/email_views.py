from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from authcore.models import GoogleCredentials
import base64
import logging
from ..models.emails import Email
from email.utils import parsedate_tz, mktime_tz
from datetime import datetime
import re
from django.utils import timezone

# Setting up logging
logger = logging.getLogger(__name__)

class ReadEmailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_email_body(self, msg):
        """Fetch the email body, checking both plain text and HTML formats.
        Strips HTML if the email is in HTML format, cleans up extra spaces, and removes URLs.
        """
        mail_text = None
        raw_html = None
        if 'parts' in msg['payload']:
            for part in msg['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    mail_text = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                elif part['mimeType'] == 'text/html':
                    raw_html = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
        else:
            raw_html = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8')
            
        
        # Remove URLs (such as the ones you provided in angle brackets or normal URL format)
        
        return raw_html, mail_text

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
            results = service.users().messages().list(userId='me', maxResults=10, q="mahaalert@mahabank.co.in").execute()
            print(results)
            messages = results.get('messages', [])

            # If no new emails, return a message
            if not messages:
                return Response({"message": "No new emails."}, status=200)

            # Initialize list to store emails' data
            emails_data = []

            # Process each message
            for message in messages:
                try:
                    msg = service.users().messages().get(userId='me', id=message['id']).execute()

                    # Extract email details
                    from_email = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'From'), None)
                    
                                        # Use a single regex search to handle both name and email address extraction
                    match = re.search(r'^(?P<name>.*?)\s?<(?P<email>[^>]+)>$', from_email.strip()) if from_email else None

                    # If a match is found, extract name and email address, otherwise handle as only email
                    sender_name, email_address = (match.group('name').strip(), match.group('email')) if match else (None, from_email.strip() if from_email else None)

                    subject = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'Subject'), None)
                    snippet = msg["snippet"] if msg["snippet"] else ""
                    
                   # Extract the date and parse it
                    date_str = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'Date'), None)

                    try:
                        # Clean the timezone abbreviation (e.g., "IST") from the string
                        if date_str:
                            date_str = re.sub(r'\s?[A-Za-z]{3,5}$', '', date_str)  # Remove timezone abbreviation like "IST"
                            
                        # Now try parsing the date with the timezone offset
                        date_obj = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')

                    except ValueError:
                        # If parsing fails, handle it differently (perhaps assume UTC or fallback logic)
                        try:
                            # Attempt to parse the date assuming it doesn't have a timezone offset (fallback to UTC)
                            date_obj = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S')  # Handle missing timezone
                            date_obj = timezone.make_aware(date_obj, timezone.utc)
                        except Exception as fallback_error:
                            # Handle the fallback failure
                            logger.error(f"Failed to parse date: {str(fallback_error)}")
                            date_obj = timezone.now()  # Set to current time in case of failure



                    # Get the email body
                    raw_html, mail_text = self.get_email_body(msg)
                    
                    # Ensure html_body and text have fallback values if None
                    raw_html = raw_html or ""  # Fallback to empty string if None
                    mail_text = mail_text or ""  # Fallback to empty string if None
                    
                    if raw_html == mail_text :
                        mail_text = ""


                    email = Email.objects.create(
                        user=request.user,
                        message_id=message['id'],
                        from_email_name = sender_name,
                        from_email=email_address,
                        subject=subject,
                        date=date_obj,
                        snippet=snippet,
                        raw_text = mail_text,
                        raw_html = raw_html
                    )

                    emails_data.append(msg)
                    email.save()

                except Exception as e:
                    logger.error(f"Failed to process message ID {message['id']}: {str(e)}")
                    continue  # Skip this email and continue with the rest

            return Response(emails_data.append(messages), status=200)

        except Exception as error:
            logger.error(f"Error occurred while fetching emails: {str(error)}")
            return Response({"error": f"An error occurred: {str(error)}"}, status=500)
