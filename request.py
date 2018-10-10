import httplib2
from urllib.parse import urlencode, unquote, quote_plus

# http = httplib2.Http()
# url = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?"
#
# data = {'serviceKey':'B5vTA+wSQ0/S3w+rbawrLgVxGIdztJG1keqskxowzSHEDpWdpFdMHs69UgO4ei3R9aNDcqmjgANp49s/VhXiqw==',
#         "LAWD_CD": "11110",
#         "DEAL_YMD": "201512" }
# encoded_args = urlencode(data)
# res, content = http.request(url+encoded_args, method='GET')
# print(res)
# print(content)

import urllib3
from urllib.parse import urlencode, unquote, quote_plus

url = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?"
data = {'serviceKey':'B5vTA+wSQ0/S3w+rbawrLgVxGIdztJG1keqskxowzSHEDpWdpFdMHs69UgO4ei3R9aNDcqmjgANp49s/VhXiqw==',
        "LAWD_CD": "11110",
        "DEAL_YMD": "201512" }
encoded_args = urlencode(data)

http = urllib3.PoolManager()
r = http.request('GET', url+encoded_args)
print(r.status)
print(r.data)


