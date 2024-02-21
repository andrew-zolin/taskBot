# from google.oauth2.credentials import Credentials
# from google.auth.transport.requests import Request
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# import datetime
# import os

# # Область видимости, необходимая для работы с Google Calendar API
# SCOPES = ['https://www.googleapis.com/auth/calendar']

# def get_credentials():
#     creds = None
#     # Проверяем, есть ли сохраненные учетные данные (credentials)
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json')
#     # Если нет, запускаем процесс аутентификации
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Сохраняем учетные данные (credentials) для будущего использования
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())
#     return creds

# def create_meeting():
#     creds = get_credentials()
#     service = build('calendar', 'v3', credentials=creds)

#     event = {
#       'summary': 'Google Meet Meeting',
#       'description': 'A chance to meet and discuss',
#       'start': {
#         'dateTime': '2024-02-10T10:00:00',
#         'timeZone': 'America/Los_Angeles',
#       },
#       'end': {
#         'dateTime': '2024-02-10T11:00:00',
#         'timeZone': 'America/Los_Angeles',
#       },
#       'conferenceData': {
#         'createRequest': {
#           'requestId': 'some-random-string-id',
#           'conferenceSolutionKey': {
#             'type': 'hangoutsMeet'
#           }
#         }
#       },
#     }

#     event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
#     print('Event created: %s' % (event.get('htmlLink')))

# if __name__ == '__main__':
#     create_meeting()