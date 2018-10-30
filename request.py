import httplib2
from urllib.parse import urlencode, unquote, quote_plus

import urllib3
from urllib.parse import urlencode, unquote, quote_plus
from real_estate_ex1 import Local_code





def make_restfull_query(lawd_cd, deal_ymd) :
        url = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?"
        data = {
                'serviceKey': 'B5vTA+wSQ0/S3w+rbawrLgVxGIdztJG1keqskxowzSHEDpWdpFdMHs69UgO4ei3R9aNDcqmjgANp49s/VhXiqw=='
        }
        data['LAWD_CD'] = lawd_cd
        data['DEAL_YMD'] = deal_ymd

        encoded_args = urlencode(data)

        http = urllib3.PoolManager()
        ret = http.request('GET', url + encoded_args)

        return ret

def print_xml(xml_str) :
        import xml.etree.ElementTree as ET
        apt_transactions = []

        xml_s = xml_str.decode('utf8')
        print(xml_s)
        root = ET.fromstring(xml_s)

        for item in root.iter('item') :
                transaction = dict()
                transaction['거래금액'] = item.find('거래금액').text
                transaction['건축년도'] = item.find('건축년도').text
                transaction['년'] = item.find('년').text
                transaction['법정동'] = item.find('법정동').text
                transaction['아파트'] = item.find('아파트').text
                transaction['월'] = item.find('월').text
                transaction['일'] = item.find('일').text
                transaction['전용면적'] = item.find('전용면적').text
                transaction['지번'] = item.find('지번').text
                transaction['지역코드'] = item.find('지역코드').text
                transaction['층'] = item.find('층').text
                print(transaction)
                apt_transactions.append(transaction)

def xml_to_dict(xml_str) :
        import xml.etree.ElementTree as ET
        apt_transactions = list()

        xml_s = xml_str.decode('utf8')
        # print(xml_s)
        root = ET.fromstring(xml_s)

        for item in root.iter('item') :
                transaction = dict()
                transaction['거래금액'] = item.find('거래금액').text
                transaction['건축년도'] = item.find('건축년도').text
                transaction['년'] = item.find('년').text
                transaction['법정동'] = item.find('법정동').text
                transaction['아파트'] = item.find('아파트').text
                transaction['월'] = item.find('월').text
                transaction['일'] = item.find('일').text
                transaction['전용면적'] = item.find('전용면적').text
                transaction['지번'] = item.find('지번').text
                transaction['지역코드'] = item.find('지역코드').text
                transaction['층'] = item.find('층').text
                print(transaction)
                apt_transactions.append(transaction)

        return apt_transactions



def find_my_apt(apt_, apt_dong, apt_name):
        my_apt_ = list()
        for apt in apt_ :
                print(apt)
                # if apt['법정동'] == apt_dong and apt['아파트'] == apt_name :
                if apt['법정동'] == apt_dong :
                        my_apt_.append(apt)
                        print(apt)

        return my_apt_


def main():
        lc = Local_code()
        lc.make_local_code()

        area_code = lc.find_area_code('고양시 일산서구')
        result = make_restfull_query(area_code, '201808')

        print(result.status)
        # print(result.data)
        # print_xml(result.data)
        apt_ = xml_to_dict(result.data)
        print(apt_)
        my_apt_ = find_my_apt(apt_, '탄현동', '탄현마을(건영4)')
        print(my_apt_)
        


        


if __name__ == '__main__' :
        main()
