from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import pytz
import dateutil.parser
from datetime import timedelta  

from fuzzywuzzy import fuzz 
from fuzzywuzzy import process 


class calendarFunctions():

    def __init__(self, credentials):
        self.credentials = credentials
        self.calendar_service = build('calendar', 'v3', credentials=credentials)
        self. utc = pytz.utc
    #-----------------------------------------------

    
    
    #-----------------------------------------------
    def to_iso8601(self, when):
        tz = pytz.timezone('Europe/Berlin')
        if not when:
            when = datetime.datetime.now(tz)
        if not when.tzinfo:
            when = tz.localize(when)
        _when = when.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        return _when[:-8] + _when[-5:] # Remove microseconds
    #-----------------------------------------------

    def from_iso8601(self, when):
        tz = pytz.timezone('Europe/Berlin')
        _when = dateutil.parser.parse(when)
        if not _when.tzinfo:
            _when = tz.localize(_when)
        return _when
    #-----------------------------------------------

# param@ numResults: the number of upcoming events listed
# return@ listDictEvents: a list of dictionaries of properties for events
    def calendarUpcoming(self, numResults = 10, calendar_id = 'primary'):
        listDictEvents =[]
        print(numResults, calendar_id)
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = self.calendar_service.events().list(calendarId=calendar_id, timeMin=now,
                                            maxResults= numResults , singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            listDictEvents.append({'summary': event['summary'], 'start': start, 'end': end, 'id': event['id'], 'reminders': event['reminders'], 'organizer': event['organizer'], 'creator' : event['creator'] })

        return listDictEvents

# param@ None:
# return@ listDictEvents: a list of dictionaries of properties for events
    def calendarsList(self):
        listDictCalendars =[]
        page_token = None
        while True:
            calendar_list = self.calendar_service.calendarList().list(pageToken=page_token).execute()
            # print(calendar_list)
            for calendar_list_entry in calendar_list['items']:
                print ("Summary: ", calendar_list_entry['summary'])
                print ("ID: ", calendar_list_entry['id'])
                listDictCalendars.append({'summary': calendar_list_entry['summary'], 'ID': calendar_list_entry['id']})
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
        return listDictCalendars


    def calendarSearchEventByName(self, query, calendar_id= 'primary'):
        events = self.calendarListAllEvents(calendar_id)
        query_results = []
        for event in events:
            similarity_ratio = fuzz.ratio(event['summary'], query) 
            if(similarity_ratio > 50):
                query_results.append(event)
        return query_results


# param@ calendar_id: passing the ID of the calendar
# return@ listDictEvents: a list of dictionaries of properties for events
    def calendarListAllEvents(self, calendar_id = 'primary'):
        listDictEvents =[]
        page_token = None
        while True:
            events = self.calendar_service.events().list(calendarId = calendar_id , pageToken=page_token).execute()
            for event in events['items']:
                print (event['summary'])
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                listDictEvents.append({'summary': event['summary'], 'start': start, 'end': end, 'id': event['id'], 'reminders': event['reminders'], 'organizer': event['organizer'], 'creator' : event['creator'] })

            page_token = events.get('nextPageToken')
            if not page_token:
                break
        return listDictEvents


# param@ date: starting date in the format of : '2019-11-07T12:00:00-08:00'
# param@ calendar_id: The calendar chosen
# return@ listDictEvents: a list of dictionaries of properties for events
    def calendarListEventsDay(self, date, calendar_id = 'primary'):
        listDictEvents =[]
        page_token = None
        # string = '2019-11-07T12:00:00-08:00'
        # listString = list(date)
        # value= int(listString[9]) + 1
        # listString[9] = str(value)
        # next_date = "".join(listString)

        print("date: ", date)


        datetime_val = self.from_iso8601( date )
        newTime = datetime_val + timedelta(days=1)  
        next_date = self.to_iso8601( newTime )

        print("Date is ", date)
        print("Next is ", next_date)

        while True:
            events = self.calendar_service.events().list(calendarId = calendar_id, timeMin = date, timeMax= next_date, pageToken=page_token).execute()
            for event in events['items']:
                print (event['summary'])
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                listDictEvents.append({'summary': event['summary'], 'start': start, 'end': end, 'id': event['id'], 'reminders': event['reminders'], 'organizer': event['organizer'], 'creator' : event['creator'] })
            page_token = events.get('nextPageToken')
            if not page_token:
                break
        return listDictEvents


# param@ time_min: in the weird format, enter in a start time 2019-11-07T12:00:00-08:00
# param@ time_max: in the weird format, enter in an end time 2019-11-07T12:00:00-08:00
# param@ calendar_id: The calendar chosen
# return@ listDictEvents: a list of dictionaries of properties for events
    def calendarListEventsWithinTime(self, time_min, time_max, calendar_id = 'primary'):
        listDictEvents =[]
        page_token = None
        while True:
            events = self.calendar_service.events().list(calendarId = calendar_id , timeMin = time_min, timeMax= time_max, pageToken=page_token).execute()
            for event in events['items']:
                print (event['summary'])
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                listDictEvents.append({'summary': event['summary'], 'start': start, 'end': end, 'id': event['id'], 'reminders': event['reminders'], 'organizer': event['organizer'], 'creator' : event['creator'] })
            page_token = events.get('nextPageToken')
            if not page_token:
                break
        return listDictEvents

# param@ input_text: input text, like "hanging with the bois on 4pm at friday"
# param@ calendar_id: The calendar chosen
# return@ none
    def calendarQuickAdd(self, input_text, calendar_id = 'primary'):
        created_event = self.calendar_service.events().quickAdd(
        calendarId = calendar_id,
        text= input_text ).execute()
        print (created_event['id'])


# param@ event_id: id of the event
# param@ calendar_id: The calendar chosen
# return@ none
    def calendarDelete(self, event_id, calendar_id = 'primary'):
        self.calendar_service.events().delete(calendarId= calendar_id, eventId= event_id).execute()


# param@ event_id: ID of the event
# param@ calendar_id: The calendar chosen
# return@ event: a json/dictionary format of all the data for that event.
    def calendarGetEvent(self, event_id, calendar_id = 'primary'):
        event = self.calendar_service.events().get(calendarId='primary', eventId='eventId').execute()
        return event


# param@ event_id: ID of the event
# param@ calendar_id: The calendar chosen
# return@ updated_event: a json/dictionary format of all the data for that event.
    def calendarEmailPopUpReminders(self, event_id, calendar_id = 'primary'):
        # First retrieve the event from the API.
        event = self.calendar_service.events().get(calendarId= calendar_id, eventId= event_id).execute()

        event['reminders']['useDefault'] = False

        event['reminders']['overrides'] = [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ]
        # print(event)
        updated_event = self.calendar_service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
        # Print the updated date.
        print (updated_event['updated'])
        payload = [updated_event]
        return payload
