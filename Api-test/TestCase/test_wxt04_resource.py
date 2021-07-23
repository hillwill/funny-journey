import sys
sys.path.append("D:\\MyProject\\Api-test")
from urllib import parse
import allure
import pytest
import requests
import yaml
from time import sleep
from common import common
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

@allure.title("新建操作员成功!")
@pytest.mark.parametrize("opeinfo, expected",
                         [
                             ({"userName": "wxt",
                               "roleType": 3}, "success"),
                         ])
def test_create_operator(login_oldadmin, opeinfo, expected):
    file = open('D:\\MyProject\\Api-test\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'],  res['operator_url'])
    print(f'url:{url}')
    method = res['operator_method']
    print(f'method:{method}')
    header = res['operator_headers']
    print(f'header:{header}')
    cookie = login_oldadmin
    print(f'cookie:{cookie}')
    print(f'opeinfo:{opeinfo}')
    s = common.Webrequests()
    response = s.run_main(method, url, opeinfo, header, cookie)
    print(response)
    assert response['status'] == expected
    sleep(5)

# @allure.title("新建指纹池成功!")
# @pytest.mark.parametrize("fpinfo, expected",
#                          [
#                              ({"fpName": "zwc",
#                                "nodeNum": "1"}, "success"),
#                          ])
# def test_create_fingerpool(login_oldsadmin, fpinfo, expected):
#     file = open('D:/MyProject/Api-test/TestData/config.yaml', encoding='utf-8')
#     res = yaml.load(file, Loader=yaml.FullLoader)
#     url = parse.urljoin(res['base_url'], res['fp_url'])
#     print(f'url:{url}')
#     # url = res['base_url']
#     method = res['fp_method']
#     print(f'method:{method}')
#     header = res['fp_headers']
#     print(f'header:{header}')
#     cookie = login_oldsadmin
#     print(f'cookie:{cookie}')
#     nodeIp = res['hostname']
#     fpinfo['nodeIps'] = [nodeIp]
#     print(f'fpinfo:{fpinfo}')
#     # s = common.Webrequests()
#     response = requests.post(url=url, data=fpinfo, headers=header, cookies=cookie, verify=False).json()
#     # response = s.run_main(method, url, fpinfo, header, cookie)
#     print(response)
#     assert response['status'] == expected

if __name__ == "__main__":
    pytest.main(["test_wxt04_resource.py"])