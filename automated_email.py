from __future__ import print_function

import base64
from email.message import EmailMessage
import os.path


import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from html_template_email import ORDER_CONFIRMED_EMAIL

import base64
from email.message import EmailMessage

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.send','https://www.googleapis.com/auth/gmail.compose']


def gmail_send_email(email, subject, content):
    """Create and insert a draft email.
       Print the returned draft's message and id.
       Returns: Draft object, including draft id and message meta data.

      Load pre-authorized user credentials from the environment.
      TODO(developer) - See https://developers.google.com/identity
      for guides on implementing OAuth2 for the application.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes=SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # create gmail api client
        service = build('gmail', 'v1', credentials=creds)

        message = EmailMessage()

        message.set_content(content)
        message.set_content(content, subtype='html')

        message['To'] = email
        message['From'] = 'amaytewari@gmail.com'
        message['Subject'] = subject

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # create_message = {
        #     'message': {
        #         'raw': encoded_message
        #     }
        # }

        create_message = {
            'raw': encoded_message
        }
        # pylint: disable=E1101
        # draft = service.users().drafts().create(userId="me",
        #                                         body=create_message).execute()
        send_message = (service.users().messages().send
                (userId="me", body=create_message).execute())

        # print(F'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')
        print(F'Message Id: {send_message["id"]}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None

    return send_message


if __name__ == '__main__':
    gmail_send_email("amay.tewari@yale.edu", "Test Email", """Hi Kishan!<br>hope this works""")