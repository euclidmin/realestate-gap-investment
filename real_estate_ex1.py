import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import pprint
from google.cloud import translate


# noinspection SpellCheckingInspection
def get_worksheet_client():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'), scope)
    client = gspread.authorize(creds)
    return client


# noinspection SpellCheckingInspection
def get_sheet(client):
    wsheet = client.open('소형아파트투자')
    sheet = wsheet.worksheet('보유현황')
    # wsheet = client.open("")
    # sheet = wsheet.worksheet('보유현황')
    return sheet


def get_col_data(sheet, index):
    col = sheet.col_values(index)
    return col


def main():
    ws_client = get_worksheet_client()
    sh = get_sheet(ws_client)

    col_A = get_col_data(sh, 1)
    print(col_A)


if __name__ == '__main__':
    main()
