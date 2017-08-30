import gspread
from oauth2client.service_account import ServiceAccountCredentials

class SpreadsheetLogger(object):

    def __init__(self, ss_name, wksht_name):
        self.spreadsheet_name = ss_name
        self.worksheet_name = wksht_name
        self.sheet = None

        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)
        try:
            self.sheet = client.open(self.spreadsheet_name).worksheet(self.worksheet_name)
        except:
            pass

    def write_to_ss(self, row_data):
        if self.sheet:
            self.sheet.append_row(row_data)
        else:
            print("WARNING: Could not find workbook %s sheet %s" % (self.spreadsheet_name, self.worksheet_name))
