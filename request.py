import httplib2
from urllib.parse import urlencode, unquote, quote_plus

import urllib3
from urllib.parse import urlencode, unquote, quote_plus

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



        
def main():
        result = make_restfull_query('41287', '201809')
        print(result.status)
        # print(result.data)
        print_xml(result.data)
        


if __name__ == '__main__' :
        main()
