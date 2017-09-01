import gspread

from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials

#
# Handle logging for the application
# use_gdrive in config.json will determine if we should log
# to a spreadsheet or print
#
class CSLogger(object):

    def __init__(self, use_gdrive, ss_name, wksht_name):
        self.sheet = None
        
        if use_gdrive:
            self.spreadsheet_name = ss_name
            self.worksheet_name = wksht_name

            scope = ['https://spreadsheets.google.com/feeds']
            creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
            client = gspread.authorize(creds)
            try:
                self.sheet = client.open(self.spreadsheet_name).worksheet(self.worksheet_name)
            except:
                pass

    def log(self, row_data):
        #get the time and add it to the row values
        now_mtn = datetime.now() + timedelta(hours=-6)
        row_data.insert(0, str(now_mtn))

        # if we have a sheet, we're logging to google drive sheet, else stdout
        if self.sheet:
            self.sheet.append_row(row_data)
        else:
            print(row_data)
