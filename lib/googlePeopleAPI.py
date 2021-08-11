from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os.path

def connect():
	SCOPES = ['https://www.googleapis.com/auth/contacts']
	creds = None

	# Check if 'token.json' exist or not
	if os.path.exists('token.json'):
		creds = Credentials.from_authorized_user_file('token.json', SCOPES)
	# If there are no (valid) credentials available, let the user log in
	if not creds or not creds.valid:
		if not creds:
			flow = InstalledAppFlow.from_client_secrets_file(
				'credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		elif creds.expired and creds.refresh_token:
			creds.refresh(Request())
		# Save the credentials for the next run
		with open('token.json', 'w') as token:
			token.write(creds.to_json())

	# Create service
	global service
	service = build('people', 'v1', credentials=creds)

def importContacts(mails):
	for mail in mails:
		# Import the mail as a contact to the account
		service.people().createContact(body={'emailAddresses': [{'value': mail}]}).execute()

def downloadContacts():
	results = service.people().connections().list(
				pageSize=1000,
				resourceName='people/me',
				personFields='names,photos,emailAddresses,metadata').execute()
	return results.get('connections', [])

def deleteContact(name):
	service.people().deleteContact(resourceName=name).execute()