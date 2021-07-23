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
from requests.adapters import HTTPAdapter

@allure.title("初始化sadmin成功!")
@pytest.mark.parametrize("initsadmin, expected",
                         [
                             ({"isEnc": "true",
                               "oldUserPass": "DN5+zryo6mSfoOjYIYKD44PlWtjxaF5YkBZPWQ2XDiJ0zJaLboHnLzKA+nl9feKJjFgK5aGDURI4rHQpU2cfJSndi/ikG3HSD3vVC1z1v2G+0PF65iWEhfZ8Rm7JRDwyqBBnC8Tclzkm28APmApkR527So0SVY92ay4m/LCL7NI=",
                               "userPass": "LDm5VpovKEISErwLXkd4AheRJ/bQ4j87gqo/QjrOw7Exc0cZLN/+ii1lVwh1rX0zchhlGt85W/s+HF6+uZ5II6vZ8Q3wdaCcYTxXY/xwgiRZnLK4jGf4tyr5M5BTTnv0JYbCE+L4VZzynlxpmh8eloQYKX9/av3T0cp40xpsBdM=",
                               "repeatUserPass": "LDm5VpovKEISErwLXkd4AheRJ/bQ4j87gqo/QjrOw7Exc0cZLN/+ii1lVwh1rX0zchhlGt85W/s+HF6+uZ5II6vZ8Q3wdaCcYTxXY/xwgiRZnLK4jGf4tyr5M5BTTnv0JYbCE+L4VZzynlxpmh8eloQYKX9/av3T0cp40xpsBdM="}, "success"),
                         ])

def test_init_sadmin(login_newsadmin, initsadmin, expected, sadmin_idSet):
    file = open('D:\\MyProject\\Api-test\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['init_url']).format(sadmin_idSet)
    header = res['init_headers']
    method = res['init_method']
    cookie = login_newsadmin
    userId = sadmin_idSet
    initsadmin['userId'] = userId
    print(url, header, method, userId)
    initsadmin['userId'] = userId
    s = common.Webrequests()
    response = s.run_main(method, url, initsadmin, header, cookie)
    print(response)
    assert response['status'] == expected
    sleep(5)

@allure.title("分配客户端成功!")
@pytest.mark.parametrize("disinfo, expected",
                         [
                             ({"clientIsBuildin": "false",
                               "nodeIp": "10.2.12.75",
                               "requestId": "ede218f8f30c11ea82ac0050568287cb",
                               "userNames": ["wxt"]}, "success"),
                         ])
def test_assign_client(login_oldsadmin, disinfo, expected, client_idSet):
    file = open('D:\\MyProject\\Api-test\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['distribution_url'])
    print(f'url:{url}')
    header = res['distribution_headers']
    print(f'header:{header}')
    method = res['distribution_method']
    print(f'method:{method}')
    cookie = login_oldsadmin
    clientId = [client_idSet]
    disinfo['ids'] = clientId
    s = requests.Session()
    s.mount(url, HTTPAdapter(max_retries=10))
    response = s.post(url, json=disinfo, headers=header, verify=False, cookies=cookie, timeout=2).json()
    assert response['responseData']['isFinished'] == expected
    sleep(5)

# @allure.title("分配指纹池成功!")
# @pytest.mark.parametrize("fpinfo, expected",
#                          [
#                              ({"fpName": "zwc",
#                                "usernames": ["wxt"]}, "success"),
#                          ])
# def test_fpdistribution(login_oldsadmin, fpinfo, expected, fp_idSet):
#     file = open('D:\\MyProject\\Api-test\\TestData\\config.yaml', encoding='utf-8')
#     res = yaml.load(file, Loader=yaml.FullLoader)
#     url = parse.urljoin(res['base_url'], res['fpdistribution_url'])
#     print(f'url:{url}')
#     header = res['fpdistribution_headers']
#     print(f'header:{header}')
#     method = res['fpdistribution_method']
#     print(f'method:{method}')
#     cookie = login_oldsadmin
#     fpId = fp_idSet
#     fpinfo['fpId'] = fpId
#     s = common.Webrequests()
#     response = s.run_main(method, url, fpinfo, header, cookie)
#     print(response)
#     assert response['status'] == expected
#     sleep(5)

if __name__ == "__main__":
    pytest.main(["test_wxt05_sadmininit&assign.py"])