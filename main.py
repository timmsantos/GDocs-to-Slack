from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()
load_dotenv(verbose=True)

from pathlib import Path 
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

slack_webhook = os.getenv("SLACK_WEBHOOK_URL")
CREDENTIALS_FILE = os.getenv ("CREDENTIALS")

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

# The ID of a sample document.
#DOCUMENT_ID = '1EYVk_r2EIa5Cj3PrRu_LA8OUNDA73MMsYjHE6S2wtSI'
DOCUMENT_ID = os.getenv('DOCUMENT_ID')

def main():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('docs', 'v1', credentials=creds)

    # Retrieve the documents contents from the Docs service.
    document = service.documents().get(documentId=DOCUMENT_ID).execute()
    getContent = document.get('body').get('content')[1].get('paragraph').get('elements')[0].get('textRun').get('content')
    slack_msg = {"text":getContent, "username":"TimBothy"}
    requests.post(slack_webhook, data=json.dumps(slack_msg))

if __name__ == '__main__':
    main()