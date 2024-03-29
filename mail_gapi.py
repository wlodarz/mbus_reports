#!/usr/bin/python3

import os
import smtplib
from email.message import EmailMessage
import mimetypes
import base64

import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class GAPI_Mail:
    sent_from = '"Bukowa BMS" <wlktest128@gmail.com>'
    # to = ['faktury@mq.energy']
    to = ['wk@poczta.fm']
    bcc = ['wlodarz@gmail.com']
    subject = 'Odczyt liczników za okres '
    body = 'This is a test'

    # gmail_server = 'smtp.gmail.com'
    # gmail_server_port = 465
    # gmail_login = 'wlktest128@gmail.com'
    # gmail_password = 'Alamakota123,'

    email_text = """From %s\nTo: %s\nSubject: %s\n\n%s""" % (sent_from, ", ".join(to), subject, body)

    def __init__(self):
        pass

    def gmail_authenticate(self):
        creds = None
        # the file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)
        # if there are no (valid) credentials availablle, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.gmail_api_scopes)
                creds = flow.run_local_server(port=0)
            # save the credentials for the next run
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)

        return build('gmail', 'v1', credentials=creds)

    def send_message(self, service, destination, obj, body, attachments=[]):
        return service.users().messages().send(
            userId="me",
            body=build_message(destination, obj, body, attachments)
        ).execute()

    def send(self, date_string, report_filename):
        try: 
            msg = EmailMessage()
            msg['Subject'] = self.subject + date_string
            msg['From'] = self.sent_from
            msg['To'] = ', '.join(self.to)
            msg['Bcc'] = ', '.join(self.bcc)
            msg['Body'] = self.body

            ctype, encoding = mimetypes.guess_type(report_filename)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)

            with open(report_filename, 'rb') as fp:
                data = fp.read()
            msg.add_attachment(data, maintype = maintype, subtype = subtype, filename=report_filename)

            service = self.gmail_authenticate()

            raw = base64.urlsafe_b64encode(msg.as_bytes())
            raw = raw.decode()

            return service.users().messages().send(
                userId="me",
                body = {'raw' : raw}
            ).execute()

            return True

        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)

            return False

if __name__=='__main__':
    api = GAPI_Mail()
    api.send('07.2022', 'odczyty_9_9_2022.pdf')

