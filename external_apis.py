from __future__ import print_function

import functools
import json
import os

import flask

from authlib.client import OAuth2Session
import google.oauth2.credentials
import googleapiclient.discovery

import google_auth
import google_drive
from google_auth import build_credentials, get_user_info

# /index.py
from flask import Flask, request, jsonify, render_template, url_for
import os
import dialogflow
import requests
import json

import pickle
import os.path

import driveFunctions
import gmailFunctions
import calendarFunctions
import sheetsFunctions
import slidesFunctions
import docsFunctions
# import queryFunctions //store this into a different file

app = flask.Blueprint('external_apis', __name__)


functionsList = {
    
        "driveFunctions": [
        { "name": "listFiles", "desc" : "List Files", "returnInputs" : ["size"]},
        { "name": "uploadFile", "desc" : "Upload File", "returnInputs" : ["filename", "filepath", "mimetype", "folder_id"]},
        { "name": "downloadFile", "desc" : "Download File", "returnInputs" : ["file_id", "filepath"]},
        { "name": "createFolder", "desc" : "Create Folder", "returnInputs" : ["name"]},
        { "name": "searchFileName", "desc" : "Search File by Name", "returnInputs" : ["search"]},
        { "name": "searchFileFolder", "desc" : "Search Folder", "returnInputs" : ["search"]},
        { "name": "searchFullText", "desc" : "Search by Contains Text", "returnInputs" : ["search"]},
        { "name": "searchFilePermissions", "desc" : "Search By Permissions", "returnInputs" : ["search"]},
        { "name": "copyFile", "desc" : "Copy a File", "returnInputs" : ["original_file_id", "copy_title"]},
        { "name": "moveFilesBetweenFolders", "desc" : "Move a File", "returnInputs" : ["file_id", "folder_id"]},
        ]
    ,
     
        "calendarFunctions": [
        { "name": "calendarUpcoming", "desc" : "Upcoming Events", "returnInputs" : ["numResults", "calendarId"]},
        { "name": "calendarsList", "desc" : "List Calendars", "returnInputs" : ["something"]},
        { "name": "calendarListAllEvents", "desc" : "List all Events (for a calendar)", "returnInputs" : ["calendar_id"]},
        { "name": "calendarListEventsDay", "desc" : "List Events by Day", "returnInputs" : ["date (2019-11-07T12:00:00-08:00)", "calendar_id"]},
        { "name": "calendarListEventsWithinTime", "desc" : "List Events by time", "returnInputs" : ["time_min", "time_max", "calendar_id"]},
        { "name": "calendarQuickAdd", "desc" : "Quick Add Event", "returnInputs" : ["input_text", "calendar_id"]},
        { "name": "calendarDelete", "desc" : "Delete an Event", "returnInputs" : ["event_id", "calendar_id"]},
        { "name": "calendarGetEvent", "desc" : "Get Data for Event", "returnInputs" : ["event_id", "calendar_id"]},
        { "name": "calendarEmailPopUpReminders", "desc" : "Enable Reminders for Event", "returnInputs" : ["event_id", "calendar_id"]},
        { "name": "calendarSearchEventByName", "desc": "query for event", "returnInputs" : ["query", "calendar"] },
        ]
    ,
     
        "gmailFunctions": [
        { "name": "callLabels", "desc" : "List Gmail Labels"},
        { "name": "create_message", "desc" : "Create Message"},
        { "name": "create_draft", "desc" : "Create Draft"},
        { "name": "send_message", "desc" : "Send the Message" },
        { "name": "create_message_with_attachment", "desc" : "Create a Message with Attachment"},
        { "name": "ListMessagesMatchingQuery", "desc" : "List messages with query"},
        { "name": "ListMessagesWithLabels", "desc" : "List Messages with Labels"},
        { "name": "GetMessage", "desc" : "Get data for a Message", "returnInputs" : ["user_id", "email_id"]},
        { "name": "GetMimeMessage", "desc" : "Get Mime Message"},
        { "name": "create_send_message", "desc" : "Create and Send a message", "returnInputs" : ["sender", "to", "subject", "message_text"]},
        { "name": "create_send_message_attachment", "desc" : "Create and Send a message with attachment", "returnInputs" : ["sender", "to", "subject", "message_text", "file_path"]},
        { "name": "create_save_draft", "desc" : "Create and save a draft", "returnInputs" : ["sender", "to", "subject", "message_text"]},
        { "name": "ListMessagesMatchingQueryMore", "desc" : "mhm", "returnInputs" : ["sender", "to", "subject", "message_text"]}
        ]
    , 
     
        "sheetsFunctions": [
        { "name": "createSheets", "desc" : "Create a Sheet", "returnInputs" : ["title"]},
        { "name": "populateSheet", "desc" : "Populate a Sheet", "returnInputs" : ["values", "spreadsheet_id", "value_input_option", "range_name"]},
        { "name": "readSheet", "desc" : "Read data from a Sheet", "returnInputs" : ["spreadsheet_id", "range_sheet"]},
        { "name": "renameSheet", "desc" : "Rename a Sheet", "returnInputs" : ["title", "spreadsheet_id"]},
        { "name": "findAndReplace", "desc" : "Find and Replace in a Sheet", "returnInputs" : ["find", "replace", "spreadsheet_id"]}
        ]
    ,
     
        "slidesFunctions": [
        { "name": "createSlides", "desc" : "Create a Slides", "returnInputs" : ["title"]},
        { "name": "createSingleSlide", "desc" : "Add a Slide to Slides", "returnInputs" : ["presentation_id", "chosen_layout"]},
        { "name": "writeShapesSlides", "desc" : "Add Textbox", "returnInputs" : ["textInput", "presentation_id", "page_id", "element_id", "xLoc", "yLoc"]}
        ]
    ,
     
        "docsFunctions": [
        { "name": "createBlankDoc", "desc" : "Create a Doc", "returnInputs" : ["title"] },
        { "name": "insertTextDoc", "desc" : "Insert Text into Doc", "returnInputs" : ["text", "document_id", "input_index"]},
        { "name": "deleteTextDoc", "desc" : "Delete Text in a Doc", "returnInputs" : ["document_id", "startIndex", "endIndex"]},
        ]
    ,
     
        "queryFunctions": [
        { "name": "wolframAlphaQuery", "desc" : "Ask Wolfram Alpha", "returnInputs" : ["query"]},
        { "name": "search_wiki", "desc" : "Search Wikipedia", "returnInputs" : ["query"]}
        ]
} 


def findClassName(query, functionList):
    for(index, classQuery) in enumerate (functionsList):
        for (index, func) in enumerate(functionsList[classQuery]):
            if func['name'] == query:
                return classQuery
    return None


# Sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    if google_auth.is_logged_in():
        print (request.url)
        numList = request.args.get('numList') #if key doesn't exist, returns None
        credentials = build_credentials()
        driveInstance = driveFunctions.driveFunctions(credentials)
        # items = driveInstance.listFiles(numList)
        items = getattr(driveInstance, 'listFiles')(numList)
        return jsonify(items)


# Sanity check route
@app.route('/functionList', methods=['GET'])
def getDriveFunctionList():
    return jsonify(functionsList)



# Sanity check route
@app.route('/callFunction', methods=['GET'])
def callFunction():
    if google_auth.is_logged_in():
        print(request.url)
        functionName = request.args.get('function') #if key doesn't exist, returns None
        value1 = request.args.get('value1') #if key doesn't exist, returns None
        value2 = request.args.get('value2') #if key doesn't exist, returns None
        value3 = request.args.get('value3') #if key doesn't exist, returns None
        value4 = request.args.get('value4') #if key doesn't exist, returns None
        print("Function: ", functionName)
        print("Value1: ", value1)
        print("Value2: ", value2)
        print("Value3: ", value3)
        print("Value4: ", value4)

        listVals = []
        if(value1):
            listVals.append(value1)
        if(value2):
            listVals.append(value2)
        if(value3):
            listVals.append(value3)
        if(value4):
            listVals.append(value4)

        credentials = build_credentials()

        classInstanceName = findClassName(functionName, functionsList)
        print("Class Instance Name: ", classInstanceName)

        if(classInstanceName == 'driveFunctions'):
            googleInstance = driveFunctions.driveFunctions(credentials)

        elif(classInstanceName == 'calendarFunctions'):
            print("do this")
            googleInstance = calendarFunctions.calendarFunctions(credentials)

        elif(classInstanceName == 'gmailFunctions'):
            print("do this")
            googleInstance = gmailFunctions.gmailFunctions(credentials)

        elif(classInstanceName == 'sheetsFunctions'):
            print("do this")
            googleInstance = sheetsFunctions.sheetsFunctions(credentials)

        elif(classInstanceName == 'slidesFunctions'):
            print("do this")
            googleInstance = slidesFunctions.slidesFunctions(credentials)

        elif(classInstanceName == 'docsFunctions'):
            print("do this")
            googleInstance = docsFunctions.docsFunctions(credentials)

        # elif(classInstanceName == 'queryFunctions'):
        #     print("do this")
        #     googleInstance = docsFunctions.docsFunctions(credentials)

        else:
            print("No class Instance")


        items = getattr(googleInstance, functionName)(*listVals)


        return jsonify(items)
    else:
        return jsonify("log in please")

