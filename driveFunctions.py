from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
import os, io

class driveFunctions():

    def __init__(self, credentials):
        self.credentials = credentials
        self.drive_service = build('drive', 'v3', credentials=credentials)


# @param size: the number of files you want to list from the drive
# @return items: a list of dictionaries is returned with {'id': id_value, 'name': file_name}
    def listFiles(self, size):
        # Call the Drive v3 API
        results = self.drive_service.files().list(
            pageSize=size, fields="nextPageToken, files(id, name, kind, mimeType)").execute()
        items = results.get('files', [])
                
        return items


# @param filename: The name of the file you are downloading
# @param filepath: where in the directory the file you are uploading is
# @param mimetype: the type of the file you are uploading
# @param folder_id: the file will be placed inside this folder if specified. If not specified then just root folder

# @return file.get('id'): the file id will be returned
    def uploadFile(self, filename, filepath, mimetype, folder_id = None):
        if(folder_id == None):
            file_metadata = {'name': filename}
        else:
            file_metadata = {'name': filename, 'parents': [folder_id]}
        
        media = MediaFileUpload(filepath, mimetype=mimetype)

        file = self.drive_service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        print ('File ID: %s' % file.get('id'))
        return file.get('id')



# @param file_id : pass in the file id that you want to download
# @param filepath : pass in the filepath you wanted the file to be saved to.

    def downloadFile(self, file_id, filepath):
        request = self.drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print ("Download %d%%." % int(status.progress() * 100))
        with io.open(filepath, 'wb') as f:
            fh.seek(0)
            f.write(fh.read())

        

# @params name: the name of the folder created

# @return file.get('id'): file id of the created folder
    def createFolder(self, name):
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        file = self.drive_service.files().create(body=file_metadata,
                                            fields='id').execute()
        # print ('Folder ID: %s' % file.get('id'))

        return file.get('id')




# @params search: pass in the string you want to query

# @return returnedList: a list of dictionaries is returned with {'id': id_value, 'name': file_name}
    def searchFileName(self, search):
        page_token = None
        returnedList = []
        query = "name contains '%s'" % search

        while True:
            response = self.drive_service.files().list(q = query,
                                                spaces='drive',
                                                fields='nextPageToken, files(id, name)',
                                                pageToken=page_token).execute()
            # print(response)
            for file in response.get('files', []):
                # Process change
                
                print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                # returnedList.update( {file.get('id') : file.get('name')} )
                returnedList.append( {'id': file.get('id'), 'name': file.get('name'), 'mimeType': file.get('mimeType')} )

            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return returnedList


# @params search: pass in the string you want to query

# @return returnedList: a list of dictionaries is returned with {'id': id_value, 'name': file_name}
    def searchFileFolder(self, search):
        returnedList = []
        page_token = None
        query = "name contains '%s' and mimeType = 'application/vnd.google-apps.folder'" % search

        while True:
            response = self.drive_service.files().list(q = query,
                                                spaces='drive',
                                                fields='nextPageToken, files(id, name)',
                                                pageToken=page_token).execute()
            for file in response.get('files', []):
                # Process change
                print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                # returnedList.update( {file.get('id') : file.get('name')} )
                returnedList.append( {'id': file.get('id'), 'name': file.get('name'), 'mimeType': file.get('mimeType')} )
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return returnedList



# @params search: pass in the string you want to query
# @return returnedList: a list of dictionaries is returned with {'id': id_value, 'name': file_name}
    def searchFullText(self, search):
        returnedList = []
        page_token = None
        query = "fullText contains '%s'" % search

        while True:
            response = self.drive_service.files().list(q = query,
                                                spaces='drive',
                                                fields='nextPageToken, files(id, name)',
                                                pageToken=page_token).execute()
            for file in response.get('files', []):
                # Process change
                print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                # returnedList.update( {file.get('id') : file.get('name')} )
                returnedList.append( {'id': file.get('id'), 'name': file.get('name'), 'mimeType': file.get('mimeType')} )
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return returnedList



# @params search: pass in the string you want to query
# @return returnedList: a list of dictionaries is returned with {'id': id_value, 'name': file_name}
    def searchFilePermissions(self, search):
        page_token = None
        returnedList = []
        query = "'%s' in writers" % search

        while True:
            response = self.drive_service.files().list(q = query,
                                                spaces='drive',
                                                fields='nextPageToken, files(id, name)',
                                                pageToken=page_token).execute()

            for file in response.get('files', []):
                # Process change
                print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                # returnedList.update( {file.get('id') : file.get('name')} )
                returnedList.append( {'id': file.get('id'), 'name': file.get('name'), 'mimeType': file.get('mimeType')} )
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        return returnedList


    def copyFile(self, origin_file_id, copy_title):
        """Copy an existing file.

        Args:
            service: Drive API service instance.
            origin_file_id: ID of the origin file to copy.
            copy_title: Title of the copy.

        Returns:
            The copied file if successful, None otherwise.
        """
        copied_file = {'title': copy_title}

        try:
            response = self.drive_service.files().copy(
                fileId=origin_file_id, body=copied_file).execute()
            return response 
            # {'kind': 'drive#file', 'id': '1-UuzPyelqdVgKcWiqlHDi5VpQH3xcmGu', 'name': 'randomimage.jpg', 'mimeType': 'image/jpeg'}

        except errors.HttpError as error:
            print ('An error occurred: %s' % error)
        return None



    def moveFilesBetweenFolders(self, file_id, folder_id):
        # Retrieve the existing parents to remove
        moveFile = self.drive_service.files().get(fileId=file_id,
                                        fields='parents').execute()
        previous_parents = ",".join(moveFile.get('parents'))
        # Move the file to the new folder
        moveFile = self.drive_service.files().update(fileId=file_id,
                                            addParents=folder_id,
                                            removeParents=previous_parents,
                                            fields='id, parents').execute()
        return moveFile

        


 