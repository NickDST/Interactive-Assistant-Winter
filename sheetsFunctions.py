from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from io import StringIO
import csv

class sheetsFunctions():

    def __init__(self, credentials):
        self.credentials = credentials
        self.sheets_service = build('sheets', 'v4', credentials = credentials)

    def createSheets(self, title):
        spreadsheet = {
        'properties': {
            'title': title
                }
            }
        spreadsheet = self.sheets_service.spreadsheets().create(body=spreadsheet,
                                            fields='spreadsheetId').execute()
        # print('Spreadsheet ID: {0}'.format(spreadsheet.get('spreadsheetId')))
        # payload = [{"title": doc['title'], "id": doc['documentId']}]
        payload = [spreadsheet]
        return payload


    def populateSheet(self, values, spreadsheet_id, value_input_option = 'RAW',range_name = 'A1' ):
        # insertValue = [[values]]

        # insertValue = csv.reader(values.split('\n'), delimiter=',')

        # for row in insertValue:
        #     print('\t'.join(row))
        payload = []
        my_list = values.split("|")

        for row in my_list:
            singleCSVrow = row.split(",")
            payload.append(singleCSVrow)

        insertValue = payload

        # values = [
        #     [
        #         # Cell values ...
        #     ],
        #     # Additional rows ...
        # ]
        body = {
            'values': insertValue
        }

        result = self.sheets_service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption=value_input_option, body=body).execute()
        print('{0} cells updated.'.format(result.get('updatedCells')))
        payload = [result]
        return payload



    def readSheet(self, spreadsheet_id, range_name = 'sheet1'):
        result = self.sheets_service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
        rows = result.get('values', [])
        print('{0} rows retrieved.'.format(len(rows)))
        return rows


    def renameSheet(self, title, spreadsheet_id):
        requests = []
        # Change the spreadsheet's title.
        requests.append({
            'updateSpreadsheetProperties': {
                'properties': {
                    'title': title
                },
                'fields': 'title'
            }
        })
        body = {
            'requests': requests
        }
        response = self.sheets_service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body).execute()
        payload = [response]
        return payload


    def findAndReplace(self, find, replacement, spreadsheet_id):
        # Find and replace text
        requests = []
        requests.append({
            'findReplace': {
                'find': find,
                'replacement': replacement,
                'allSheets': True
            }
        })
        body = {
            'requests': requests
        }
        response = self.sheets_service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body).execute()
        find_replace_response = response.get('replies')[1].get('findReplace')
        print('{0} replacements made.'.format(
            find_replace_response.get('occurrencesChanged')))
        payload = [find_replace_response]
        return payload