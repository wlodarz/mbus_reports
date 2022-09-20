#!/usr/bin/python3

import os
import smtplib
from email.message import EmailMessage
import mimetypes

class Mail:
    sent_from = 'wlktest128@gmail.com'
    # to = ['wlodarz@gmail.com']
    to = ['faktury@mq.energy']
    bcc = ['wlk@poczta.fm']
    subject = 'Odczyt liczników za okres '
    body = 'This is a test'

    gmail_server = 'smtp.gmail.com'
    gmail_server_port = 465
    gmail_login = 'wlktest128@gmail.com'
    # gmail_password = 'Alamakota123,' # - this is account pass
    gmail_password = 'znxrvwanshxpfpta'

    email_text = """From %s\nTo: %s\nSubject: %s\n\n%s""" % (sent_from, ", ".join(to), subject, body)

    def __init__(self):
        pass

    def send(self, date_string, report_filename):
        try: 
            msg = EmailMessage()
            msg['Subject'] = self.subject + date_string
            msg['From'] = self.sent_from
            msg['To'] = ', '.join(self.to)
            msg['Bcc'] = ', '.join(self.bcc)
            msg['Body'] = self.body
            # msg.preable = self.body

            ctype, encoding = mimetypes.guess_type(report_filename)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)

            with open(report_filename, 'rb') as fp:
                data = fp.read()
            msg.add_attachment(data, maintype = maintype, subtype = subtype, filename=report_filename)


            server_ssl = smtplib.SMTP_SSL(self.gmail_server, self.gmail_server_port)
            server_ssl.ehlo()
            server_ssl.login(self.gmail_login, self.gmail_password)
            server_ssl.send_message(msg)
            server_ssl.close()

            return True

        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)

            return False

if __name__=='__main__':
    api = Mail()
    api.send('07.2022', 'odczyty_9_9_2022.pdf')

