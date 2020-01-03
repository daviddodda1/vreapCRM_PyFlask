from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
import mimetypes
import base64
import pyotp
import pyqrcode
import png




def service_account_login():
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://mail.google.com/']

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
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    return service

def create_message_with_attachment(sender, to, subject, message_text, file):
    """Create a message for an email.

    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file: The path to the file to be attached.

    Returns:
    An object containing a base64url encoded email object.
    """
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text,_subtype='html')
    message.attach(msg)

    content_type, encoding = mimetypes.guess_type(file)
    if (content_type is not None or encoding is None):
        content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        print(11)
        fp = open(file, 'rb')
        img = MIMEImage(fp.read(), 'png')
        img.add_header('Content-Id', '<testimage>')
        fp.close()
        message.attach(img)
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode('UTF-8')).decode('ascii')}



def send_message(service, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId='me', body=message).execute())
    print ('Message Id: {}'.format(message['id']))
    return message
  except ConnectionError as error:
    print ('An error occurred: {}'.format(error))


def create_message(sender, to, subject, message_text):
    """Create a message for an email.
    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    Returns:
    An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode('UTF-8')).decode('ascii')}




def sendEmailQRcode(email, uuID):
    QR_code_url = pyotp.totp.TOTP(uuID).provisioning_uri("VREAP foundation CRM Admin", issuer_name="VREAP Foundation")
    QRcode = pyqrcode.create(QR_code_url)
    QRcode.png('./code.png', scale=4)
    service = service_account_login()
    message = create_message_with_attachment('me', email, 'hi arun this is a test',
                                             '<img src="cid:testimage" /></br> <p style="align-content: center; font-size: 1rem; margin-top: 0.5rem; padding: 0.5rem"> please scan the qrcode from the google auth app to link yout gmail account with vreap CRM</p>',
                                             './code.png')
    send_message(service, message)

