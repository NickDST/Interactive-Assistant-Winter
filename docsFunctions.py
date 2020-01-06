from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class docsFunctions():

    def __init__(self, credentials):
        self.credentials = credentials
        self.drive_service = build('docs', 'v1', credentials = credentials)


    def createBlankDoc(self, title):
        body = {
            'title': title
        }
        doc = self.drive_service.documents() \
            .create(body=body).execute()
        print('Created document with title: {0}'.format(doc.get('title')))
        payload = [{"id": doc['documentId']}]
        # print(doc['documentId'])
        return payload


    def insertTextDoc(self, text, document_id, input_index = 1):
        requests = [
         {
            'insertText': {
                'location': {
                    'index': input_index,
                },
                'text': text
            }
        } ]
        doc = self.drive_service.documents().batchUpdate(documentId = document_id, body={'requests': requests}).execute()
        # payload = [{"title": doc['title'], "id": doc['documentId']}]
        # print(doc)
        # payload = [{"id": doc['documentId']}]
        payload = [doc]
        return payload



    def deleteTextDoc(self, document_id, startIndex, endIndex):
        requests = [
        {
            'deleteContentRange': {
                'range': {
                    'startIndex': startIndex,
                    'endIndex': endIndex,
                }
            }
        } ]
        doc = self.drive_service.documents().batchUpdate(
            documentId=document_id, body={'requests': requests}).execute()
        payload = [{"title": doc['title'], "id": doc['documentId']}]
        return payload
    
