from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class slidesFunctions():

    def __init__(self, credentials):
        self.credentials = credentials
        self.slides_service = build('slides', 'v1', credentials = credentials)


# @param title: The title of the slides that will be created
    def createSlides(self, title):
        body = {
            'title': title
        }
        presentation = self.slides_service.presentations() \
            .create(body=body).execute()
        print('Created presentation with ID: {0}'.format(
            presentation.get('presentationId')))

# @param presentation_id: the ID of the presentation
# @param chosen_layout: predefined layout, some options include:
# '''UNSUPPORTED BLANK CAPTION_ONLY TITLE TITLE_AND_BODY TITLE_AND_TWO_COLUMNS TITLE_ONLY SECTION_HEADER SECTION_TITLE_AND_DESCRIPTION '''

    def createSingleSlide(self, presentation_id, chosen_layout = 'TITLE_AND_TWO_COLUMNS'):
        # Add a slide at index 1 using the predefined
        # 'TITLE_AND_TWO_COLUMNS' layout and the ID page_id.
        requests = [
            {
                'createSlide': {
                    'insertionIndex': '1',
                    'slideLayoutReference': {
                        'predefinedLayout': chosen_layout #https://developers.google.com/apps-script/reference/slides/predefined-layout
                    }
                }
            }
        ]
        # If you wish to populate the slide with elements,
        # add element create requests here, using the page_id.
        # Execute the request.
        body = {
            'requests': requests
        }
        response = self.slides_service.presentations() \
            .batchUpdate(presentationId=presentation_id, body=body).execute()
        create_slide_response = response.get('replies')[0].get('createSlide')
        print(response)
        # print('Created slide with ID: {0}'.format(
        #     create_slide_response.get('objectId')))


# @param create shapes or text and add it to the slide at a specified location. 
    def writeShapesSlides(self, textInput, presentation_id, page_id, element_id, xLoc = 100, yLoc = 100):
        # Create a new square textbox, using the supplied element ID.
        pt350 = {
            'magnitude': 350,
            'unit': 'PT'
        }
        requests = [
            {
                'createShape': {
                    'objectId': element_id,
                    'shapeType': 'TEXT_BOX',
                    'elementProperties': {
                        'pageObjectId': page_id,
                        'size': {
                            'height': pt350,
                            'width': pt350
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': 100,
                            'translateY': 100,
                            'unit': 'PT'
                        }
                    }
                }
            },

            # Insert text into the box, using the supplied element ID.
            {
                'insertText': {
                    'objectId': element_id,
                    'insertionIndex': 0,
                    'text': textInput
                }
            }
        ]

        # Execute the request.
        body = {
            'requests': requests
        }
        response = self.slides_service.presentations() \
            .batchUpdate(presentationId=presentation_id, body=body).execute()
        create_shape_response = response.get('replies')[0].get('createShape')
        print('Created textbox with ID: {0}'.format(
            create_shape_response.get('objectId')))