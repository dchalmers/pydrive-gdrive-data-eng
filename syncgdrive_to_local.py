# Script to pull 

import os as os
import shutil as sh
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

relative_dir = '../segoutput/'
input_drive_folder = 'images'

gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth)

query_string = "'root' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed=false" 
file_list = drive.ListFile({'q': query_string}).GetList()


def search(targetkey, targetvalue, dictslist):
    return [element for element in dictslist if element[targetkey] == targetvalue]

def buildLookupDict(parent_folder):
	lookupDict = {}
	parent_folder = 'images'
	# query to get parent folder ID
	query_string = "'root' in parents and title='{}' and trashed=false".format(parent_folder) 
	file_list = drive.ListFile({'q': query_string}).GetList()
	id = file_list[0]['id']
	# query for children of parent
	query_string = "'{}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed=false".format(id)
	file_list = drive.ListFile({'q': query_string}).GetList()
	# extract foldername and ID to dict
	for element in file_list:
		lookupDict[element['title']] = element['id']
		
	# return the dict
	return lookupDict
# print(str(os.getcwd()))

folders = os.listdir(relative_dir)
lookupDict = buildLookupDict(input_drive_folder)

count = 0

for fd in folders:
	query_string = "'{}' in parents and trashed=false".format(lookupDict[fd])
	file_list = drive.ListFile({'q': query_string}).GetList()
	input_folder = search('title','input',file_list)
	query_string = "'{}' in parents and trashed=false".format(input_folder[0]['id'])
	file_list = drive.ListFile({'q': query_string}).GetList()
	count = count + 1
	for infile in file_list:
		local_name = "{}{}/{}_input_{}".format(relative_dir,fd, fd, infile['title'])
		infile.GetContentFile(local_name)
		print("Downloaded {}: Folder {} of {}".format(local_name,count,len(folders)))
