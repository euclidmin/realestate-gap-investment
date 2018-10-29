import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import numpy as np
import pprint
from google.cloud import translate


class Local_code:

    def __init__(self, local_name=None):
        self.local_name = local_name
        self.lc_fullset = None
        self.lc_pairs = None
        self.pkl = {}

        self.client = None
        self.sheet = None

        import pickle
        dataset_dir = os.path.dirname(os.path.abspath(__file__))
        save_file = dataset_dir + "/localcode.pkl"

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







    def extract_data_from_sheet(self):
        def get_col_data(sheet, index):
            col = sheet.col_values(index)
            return col

        local_code = get_col_data(self.sheet, 1)
        city_state = get_col_data(self.sheet, 2)
        city_gun_gu = get_col_data(self.sheet, 3)
        eup_myen_dong = get_col_data(self.sheet, 4)

        local_code_record = []
        for a, b, c, d in zip(local_code, city_state, city_gun_gu, eup_myen_dong):
            abcd = [a, b, c, d]
            local_code_record.append(abcd)
        return local_code_record

    def extract_data_from_sheet1(self):
        def get_col_data(sheet, index):
            col = sheet.col_values(index)
            return col

        local_code = get_col_data(self.sheet, 1)
        city_state = get_col_data(self.sheet, 2)
        city_gun_gu = get_col_data(self.sheet, 3)
        eup_myen_dong = get_col_data(self.sheet, 4)

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
        def filter_dong_record():
            ret_ = []
            for lc_record in self.local_code_record:
                if lc_record[2] != '' and lc_record[3] == '':
                    ret_.append([lc_record[0], lc_record[2]])
            return ret_

        def slice_five_num(ret_):
            for pair in ret_:
                pair[0] = pair[0][0:5]

        ret_ = filter_dong_record()
        slice_five_num(ret_)
        self.save_pkl(ret_)
        self.code_local_ = ret_

        return self.code_local_

    def save_pkl(self, ret_):
        import pickle
        dataset_dir = os.path.dirname(os.path.abspath(__file__))
        save_file = dataset_dir + "/localcode.pkl"
        if self.lc_fullset is None and self.lc_pairs is None:
            self.pkl['lc_fullset'] = self.local_code_record
            self.pkl['lc_pairs'] = ret_

            with open(save_file, 'wb') as f:
                pickle.dump(self.pkl, f)
                print('save pkl file.')


    def find_area_code(self, dong_str):
        for code_local in self.code_local_ :
            if code_local[1] == dong_str :
                ret = code_local[0]
                break
            else :
                ret = None
        return ret


    def make_local_code(self):
        self.get_worksheet_client()
        self.get_sheet('KIKcd_H.20180122', 'KIKcd_H')
        self.load_local_code_data()
        self.make_code_local()
        print(self.code_local_)

def main():

    # lc = Local_code('탄현동')
    lc = Local_code()
    lc.make_local_code()

    local_code = lc.find_area_code('용산구')
    print(local_code)



if __name__ == '__main__':
    main()
