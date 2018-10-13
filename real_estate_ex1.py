import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import numpy as np
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
def get_sheet(client, wsheet_name=None, sheet_name=None):
    if wsheet_name==None :
        wsheet = client.open('소형아파트투자')
    else :
        wsheet = client.open(wsheet_name)

    if sheet_name==None :
        sheet = wsheet.worksheet('보유현황')
    else :
        sheet = wsheet.worksheet(sheet_name)
    return sheet




def get_col_data(sheet, index):
    col = sheet.col_values(index)
    return col


def extract_data_from_sheet(sheet):
    local_code = get_col_data(sheet, 1)
    city_state = get_col_data(sheet, 2)
    city_gun_gu = get_col_data(sheet, 3)
    eup_myen_dong = get_col_data(sheet, 4)

    local_code_record = []
    for a, b, c, d in zip(local_code, city_state, city_gun_gu, eup_myen_dong):
        abcd = [a, b, c, d]
        local_code_record.append(abcd)
    return local_code_record

def extract_data_from_sheet1(sheet):
    local_code = get_col_data(sheet, 1)
    city_state = get_col_data(sheet, 2)
    city_gun_gu = get_col_data(sheet, 3)
    eup_myen_dong = get_col_data(sheet, 4)

    local_code_record = np.array([local_code, city_state, city_gun_gu, eup_myen_dong]).transpose()

    print(local_code_record)
    
    return local_code_record

def load_local_code_data(sheet):
    import pickle
    dataset_dir = os.path.dirname(os.path.abspath(__file__))
    save_file = dataset_dir + "/localcode.pkl"

    if not os.path.exists(save_file):
        local_code_dataset = extract_data_from_sheet1(sheet)
        with open(save_file, 'wb') as f:
            pickle.dump(local_code_dataset, f)
            print('save pkl file.')
    with open(save_file, 'rb') as f:
        dataset = pickle.load(f)
        print('load pkl')

    return dataset





def make_local_city(lc_records):
    ret_ = []
    for lc_record in lc_records :
        if lc_record[2]!='' and lc_record[3]=='' :
            ret_.append([lc_record[0], lc_record[2]])

    for pair in ret_ :
        pair[0] = pair[0][0:5]

    return ret_


def main():
    ws_client = get_worksheet_client()
    # sh = get_sheet(ws_client)
    sh = get_sheet(ws_client, 'KIKcd_H.20180122', 'KIKcd_H')
    local_code_record = load_local_code_data(sh)
    print(local_code_record)
    localcode_cityname_ = make_local_city(local_code_record)

    print(localcode_cityname_)






if __name__ == '__main__':
    main()
