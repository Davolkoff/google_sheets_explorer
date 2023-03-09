import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


class GoogleTable:
    def __init__(self, credentials_file, spreadsheet_id):
        # регистрация и получение экземпляра доступа к API
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_file,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())
        self.service = googleapiclient.discovery.build('sheets', 'v4', http=httpAuth)
        self.spreadsheet_id = spreadsheet_id
    
    def write_values(self, sheet_name, write_type, begin, end, values):
    
        self.service.spreadsheets().values().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": f'\'{sheet_name}\'!{begin}:{end}',
                     "majorDimension": write_type,
                     "values": values}]}).execute()
    
    def read_values(self, sheet_name, read_type, begin, end):
        info = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=f'\'{sheet_name}\'!{begin}:{end}',
            majorDimension=read_type
        ).execute()
        try:
            return info["values"]
        except:
            return [""]
