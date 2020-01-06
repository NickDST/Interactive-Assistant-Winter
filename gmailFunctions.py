from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import base64
import email
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os


from apiclient import errors



class gmailFunctions():

    def __init__(self, credentials):
        self.credentials = credentials
        self.gmail_service = build('gmail', 'v1', credentials=credentials)


    def callLabels(self):
        results = self.gmail_service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        return labels


    def create_send_message(self, sender, to, subject, message_text):
        full_message = self.create_message(sender, to, subject, message_text)
        response = self.send_message('me', full_message)
        if response is not None:
            return [response]
        else:
            return "message not sent"


    def create_save_draft(self, sender, to, subject, message_text):
        full_message = self.create_message(sender, to, subject, message_text)
        response = self.create_draft('me', full_message)
        if response is not None:
            return [response]
        else:
            return "message not sent"



    def create_send_message_attachment(self, sender, to, subject, message_text, file_path):
        full_message = self.create_message_with_attachment(sender, to, subject, message_text)
        response = self.send_message('me', full_message)
        if response is not None:
            return [response]
        else:
            return "message with attachment not sent"



    def create_message(self, sender, to, subject, message_text):
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
        return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}



    def create_draft(self, user_id, message_body):
        """Create and insert a draft email. Print the returned draft's message and id.

        Args:
            service: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
            can be used to indicate the authenticated user.
            message_body: The body of the email message, including headers.

        Returns:
            Draft object, including draft id and message meta data.
        """
        try:
            message = {'message': message_body}
            draft = self.gmail_service.users().drafts().create(userId=user_id, body=message).execute()

            print ('Draft id: %s\nDraft message: %s' % (draft['id'], draft['message']))

            return draft
        except errors.HttpError as error:
            print ('An error occurred: %s' % error)
            return None




    def send_message(self, user_id, message):
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
            message = (self.gmail_service.users().messages().send(userId=user_id, body=message)
                    .execute())
            print ('Message Id: %s' % message['id'])
            return message
        except errors.HttpError as error:
            print ('An error occurred: %s' % error)
            return None



    def create_message_with_attachment(self, sender, to, subject, message_text, file):
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

        msg = MIMEText(message_text)
        message.attach(msg)

        content_type, encoding = mimetypes.guess_type(file)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            fp = open(file, 'rb')
            msg = MIMEText(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            fp = open(file, 'rb')
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(file, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(file, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()
        filename = os.path.basename(file)
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(msg)

        return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


    def ListMessagesMatchingQueryMore(self, query):
        result = self.ListMessagesMatchingQuery(query)
        dataList = []
        for value in result:
            full_value = self.GetMessage('me', value['id'])
            dataList.append({'snippet': full_value['snippet']})
        return dataList    


    def ListMessagesMatchingQuery(self, query='', user_id = 'me'):
        """List all Messages of the user's mailbox matching the query.

        Args:
            service: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
            can be used to indicate the authenticated user.
            query: String used to filter messages returned.
            Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

        Returns:
            List of Messages that match the criteria of the query. Note that the
            returned list contains Message IDs, you must use get with the
            appropriate ID to get the details of a Message.
        """
        try:
            response = self.gmail_service.users().messages().list(userId=user_id, q=query).execute()
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = self.gmail_service.users().messages().list(userId=user_id, q=query,
                                                    pageToken=page_token).execute()
                messages.extend(response['messages'])

            return messages
        except errors.HttpError as error:
            print ('An error occurred: %s' % error)



    def ListMessagesWithLabels(self, user_id = 'me', label_ids=[]):
        """List all Messages of the user's mailbox with label_ids applied.

        Args:
            service: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
            can be used to indicate the authenticated user.
            label_ids: Only return Messages with these labelIds applied.

        Returns:
            List of Messages that have all required Labels applied. Note that the
            returned list contains Message IDs, you must use get with the
            appropriate id to get the details of a Message.
        """
        try:
            response = self.gmail_service.users().messages().list(userId=user_id,
                                                    labelIds=label_ids).execute()
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = self.gmail_service.users().messages().list(userId=user_id,
                                                            labelIds=label_ids,
                                                            pageToken=page_token).execute()
                messages.extend(response['messages'])

            return messages
        except errors.HttpError as error:
            print ('An error occurred: %s' % error)



    def GetMessage(self, user_id, msg_id):
        """Get a Message with given ID.

        Args:
            service: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
            can be used to indicate the authenticated user.
            msg_id: The ID of the Message required.

        Returns:
            A Message.
        """
        try:
            message = self.gmail_service.users().messages().get(userId=user_id, id=msg_id).execute()

            print ('Message snippet: %s' % message['snippet'])

            return message
        except errors.HttpError as error:
            print ('An error occurred: %s' % error)



    def GetMimeMessage(self, user_id, msg_id):
        """Get a Message and use it to create a MIME Message.

        Args:
            service: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
            can be used to indicate the authenticated user.
            msg_id: The ID of the Message required.

        Returns:
            A MIME Message, consisting of data from Message.
        """
        try:
            message = self.gmail_service.users().messages().get(userId=user_id, id=msg_id,
                                                    format='raw').execute()

            print ('Message snippet: %s' % message['snippet'])

            msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

            mime_msg = email.message_from_string(msg_str)

            return mime_msg
        except errors.HttpError as error:
            print ('An error occurred: %s' % error)








