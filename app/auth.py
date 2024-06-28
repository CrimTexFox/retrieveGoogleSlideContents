import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/presentations.readonly']
SERVICE_ACCOUNT_FILE = 'app/credentials.json'

def get_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    service = build('slides', 'v1', credentials=credentials)
    drive_service = build('drive', 'v3', credentials=credentials)
    return service, drive_service
