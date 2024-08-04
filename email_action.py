import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import base64
from datetime import datetime, timedelta
import dateutil
from dateutil.parser import parse, isoparse


class EmailAction:

	SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
	creds = None
	
	if os.path.exists("token.json"):
	    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
	
	if not creds or not creds.valid:
	    if creds and creds.expired and creds.refresh_token:
	        creds.refresh(Request())
	    else:
	        flow = InstalledAppFlow.from_client_secrets_file(
	            "credentials.json", SCOPES
	        )
	        creds = flow.run_local_server(port=0)
	
	    with open("token.json", "w") as token:
	        token.write(creds.to_json())

	service = build('gmail', 'v1', credentials=creds)


	@classmethod
	def fetch_emails(cls):

		results = cls.service.users().messages().list(userId='me').execute()
		emails = results.get('messages', [])
		
		email_data = []

		for email in emails:
			message = cls.get_email(email['id'])

			headers = message['payload']['headers']
			from_header = next(header for header in headers if header['name'] == 'From')
			date_header = next(header for header in headers if header['name'] == 'Date')
			subject_header = next(header for header in headers if header['name'] == 'Subject')

			label_ids = message['labelIds']
			to_header = message['payload']['headers']
			recipients = next(header['value'] for header in to_header if header['name'] == 'To')

			message_id = message.get("id")
			sender = from_header['value']
			date = date_header['value']
			subject = subject_header['value']



			try:
			    date_parts = date.split()
			    date_no_tz = ' '.join(date_parts[:-1])
			    tz_offset = date_parts[-1]
			    
			    parsed_date = datetime.strptime(date_no_tz, "%a, %d %b %Y %H:%M:%S")
			    
			    tz_offset_delta = timedelta(hours=int(tz_offset[1:3]), minutes=int(tz_offset[3:]))
			    
			    if tz_offset[0] == '+':
			        parsed_date += tz_offset_delta
			    elif tz_offset[0] == '-':
			        parsed_date -= tz_offset_delta
			    
			except ValueError as e:

				parsed_date = parse(date)
				parsed_date = parsed_date.strftime("%Y-%m-%d %H:%M:%S")

			
			email_body = ''
			if 'parts' in message['payload']:
			    for part in message['payload']['parts']:
			        if part['mimeType'] == 'text/plain':
			            email_body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
			            break
			elif 'body' in message['payload']:
			    email_body = base64.urlsafe_b64decode(message['payload']['body']['data']).decode('utf-8')


			email_data.append({
				"id": message.get("id"),
				"sender": sender,
				"date": parsed_date,
				"subject": subject,
				"body": email_body,
				"recipients": recipients
				})

		return email_data

	
	@classmethod
	def get_email(cls, message_id):
	    message = cls.service.users().messages().get(userId='me', id=message_id).execute()
	    return message

	
	@classmethod
	def mark_email_read_unread(cls, id, read):
		try:
		    modify_request = {'removeLabelIds': ['UNREAD']} if read else {'addLabelIds': ['UNREAD']}
		    cls.service.users().messages().modify(userId='me', id=id, body=modify_request).execute()
		    print(f"Message with id: {id} marked as {'read' if read else 'unread'}.")
		except Exception as e:
		    print(f"An error occurred: {e}")

	@classmethod
	def move_email(cls, email_id, destination_mailbox):
		try:
			message = cls.service.users().messages().get(userId='me', id=email_id).execute()
			current_labels = message['labelIds']

			destination_label = None
			labels = cls.service.users().labels().list(userId='me').execute()
			for label in labels['labels']:
				if label['name'] == destination_mailbox:
					destination_label = label['id']

			if not destination_label:
				raise Exception("Destination label {} not present".format(destination_label))

			current_labels.append(destination_label)

			body = {'removeLabelIds': ['INBOX'], 'addLabelIds': [destination_label]}
			cls.service.users().messages().modify(userId='me', id=email_id, body=body).execute()

			print(f"Email {email_id} moved to {destination_mailbox} successfully.")

		except Exception as e:
			raise Exception(f"An error occurred: {e}")


