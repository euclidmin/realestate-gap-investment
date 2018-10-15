import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import numpy as np
import pprint
from google.cloud import translate


class Local_code:

    def __init__(self):
        import pickle
        dataset_dir = os.path.dirname(os.path.abspath(__file__))
        save_file = dataset_dir + "/localcode.pkl"
        self.pkl = {}

        if os.path.exists(save_file):
            with open(save_file, 'rb') as f:
                dataset = pickle.load(f)
                self.lc_fullset = dataset['lc_fullset']
                self.lc_pairs = dataset['lc_pairs']
                print('load pkl')
        else :
            self.lc_fullset = None
            self.lc_pairs = None



    
    # noinspection SpellCheckingInspection
    def get_worksheet_client(self):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'), scope)
        client = gspread.authorize(creds)

        self.client = client
        return client


    # noinspection SpellCheckingInspection
    def get_sheet(self, wsheet_name=None, sheet_name=None):
        if wsheet_name==None :
            wsheet = self.client.open('소형아파트투자')
        else :
            wsheet = self.client.open(wsheet_name)

        if sheet_name==None :
            sheet = wsheet.worksheet('보유현황')
        else :
            sheet = wsheet.worksheet(sheet_name)

        self.sheet = sheet
        return sheet




    def get_col_data(self, sheet, index):
        col = sheet.col_values(index)
        return col


    def extract_data_from_sheet(self):
        local_code = self.get_col_data(self.sheet, 1)
        city_state = self.get_col_data(self.sheet, 2)
        city_gun_gu = self.get_col_data(self.sheet, 3)
        eup_myen_dong = self.get_col_data(self.sheet, 4)

        local_code_record = []
        for a, b, c, d in zip(local_code, city_state, city_gun_gu, eup_myen_dong):
            abcd = [a, b, c, d]
            local_code_record.append(abcd)
        return local_code_record

    def extract_data_from_sheet1(self):
        local_code = self.get_col_data(self.sheet, 1)
        city_state = self.get_col_data(self.sheet, 2)
        city_gun_gu = self.get_col_data(self.sheet, 3)
        eup_myen_dong = self.get_col_data(self.sheet, 4)

        local_code_record = np.array([local_code, city_state, city_gun_gu, eup_myen_dong]).transpose()
        print(local_code_record)

        self.local_code_record = local_code_record
        return local_code_record

    def load_local_code_data(self):

        if self.lc_fullset is None and self.lc_pairs is None :
            self.extract_data_from_sheet1()
        else :
            print('already loaded pkl file')
            self.local_code_record = self.lc_fullset

        return self.local_code_record






    def make_code_local(self):
        import pickle
        dataset_dir = os.path.dirname(os.path.abspath(__file__))
        save_file = dataset_dir + "/localcode.pkl"

        ret_ = []
        for lc_record in self.local_code_record :
            if lc_record[2]!='' and lc_record[3]=='' :
                ret_.append([lc_record[0], lc_record[2]])

        for pair in ret_ :
            pair[0] = pair[0][0:5]

        if self.lc_fullset is None and self.lc_pairs is None :
            self.pkl['lc_fullset'] = self.local_code_record
            self.pkl['lc_pairs'] = ret_

            with open(save_file, 'wb') as f:
                pickle.dump(self.pkl, f)
                print('save pkl file.')

        self.code_local_ = ret_
        return self.code_local_


def main():

    # lc = Local_code('탄현동')
    lc = Local_code()
    lc.get_worksheet_client()
    lc.get_sheet('KIKcd_H.20180122', 'KIKcd_H')
    lc.load_local_code_data()
    lc.make_code_local()
    print(lc.code_local_)

    

    # find_localcode()





if __name__ == '__main__':
    main()
