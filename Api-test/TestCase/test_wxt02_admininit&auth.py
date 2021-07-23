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


@allure.title("初始化admin成功!")
@pytest.mark.parametrize("initadmin, expected",
                         [
                             ({"isEnc": "true",
                               "oldUserPass": "Lx+vJdrqkEcRiWTUNqfWFGQD+xvKH4wHjn22sm4iuwQvFyM2JsNXKGWqN05lkmPQaCObxiJlxnAM3SDNzT1PmMQs9pn/LTQPIAhdH9kYC1Pc25dvyH1qp9jJDymICD+gf4UIaY5WZUGicTpqOlT1dS/eI8gIabYFKH7x4ol2k3Q=",
                               "userPass": "LDm5VpovKEISErwLXkd4AheRJ/bQ4j87gqo/QjrOw7Exc0cZLN/+ii1lVwh1rX0zchhlGt85W/s+HF6+uZ5II6vZ8Q3wdaCcYTxXY/xwgiRZnLK4jGf4tyr5M5BTTnv0JYbCE+L4VZzynlxpmh8eloQYKX9/av3T0cp40xpsBdM=",
                               "repeatUserPass": "LDm5VpovKEISErwLXkd4AheRJ/bQ4j87gqo/QjrOw7Exc0cZLN/+ii1lVwh1rX0zchhlGt85W/s+HF6+uZ5II6vZ8Q3wdaCcYTxXY/xwgiRZnLK4jGf4tyr5M5BTTnv0JYbCE+L4VZzynlxpmh8eloQYKX9/av3T0cp40xpsBdM="}, "success"),
                         ])
def test_init_admin(login_newadmin, initadmin, expected, admin_idSet):
    file = open('D:\\MyProject\\Api-test\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['init_url']).format(admin_idSet)
    print(url)
    header = res['init_headers']
    print(header)
    method = res['init_method']
    print(method)
    cookie = login_newadmin
    print(cookie)
    userId = admin_idSet
    initadmin['userId'] = userId
    print(initadmin)
    s = common.Webrequests()
    response = s.run_main(method, url, initadmin, header, cookie)
    print(response)
    assert response['status'] == expected
    sleep(5)

# @allure.title("添加授权码成功!")
# @pytest.mark.parametrize("authinfo, expected",
#                          [
#                              ({"licenseCode": "A7TY0-0C0S4-5B3S9-G426C-MMQFQ-G6K5Q"}, "success"),
#                          ])
# def test_auth(login_oldadmin, authinfo, expected):
#     file = open('D:\\MyProject\\Api-test\\TestData\\config.yaml', encoding='utf-8')
#     res = yaml.load(file, Loader=yaml.FullLoader)
#     url = parse.urljoin(res['base_url'], res['auth_url'])
#     method = res['auth_method']
#     header = res['auth_headers']
#     cookie = login_oldadmin
#     s = common.Webrequests()
#     response = s.run_main(method, url, authinfo, header, cookie)
#     print(response)
#     assert response['status'] == expected
#     sleep(5)
#
# @allure.title("激活授权成功!")
# @pytest.mark.parametrize("activeinfo, expected",
#                          [
#                              ({"activeCode": "5HSSJB2D7X8YN2NJ"}, "success"),
#                          ])
# def test_active(auth_idSet, login_oldadmin, activeinfo, expected):
#     file = open('D:\\MyProject\\Api-test\\TestData\\config.yaml', encoding='utf-8')
#     res = yaml.load(file, Loader=yaml.FullLoader)
#     url = parse.urljoin(res['base_url'], res['active_url']).format(auth_idSet)
#     print(f'url:{url}')
#     method = res['active_method']
#     print(f'method:{method}')
#     header = res['active_headers']
#     print(f'header:{header}')
#     cookie = login_oldadmin
#     print(f'cookie:{cookie}')
#     s = common.Webrequests()
#     response = s.run_main(method, url, activeinfo, header, cookie)
#     print(response)
#     assert response['status'] == expected
#     sleep(5)
#
# @allure.title("添加数据传输IP成功!")
# @pytest.mark.parametrize("dtipinfo, expected",
#                          [
#                              ({"ipList": ["10.2.12.75"]}, "success"),
#                          ])
# def test_datatransferip(login_oldadmin, dtipinfo, expected, nodes_idSet):
#     file = open('D:\\MyProject\\Api-test\\TestData\\config.yaml', encoding='utf-8')
#     res = yaml.load(file, Loader=yaml.FullLoader)
#     url = parse.urljoin(res['base_url'], res['dtip_url'])
#     print(f'url:{url}')
#     method = res['dtip_method']
#     print(f'method:{method}')
#     header = res['dtip_headers']
#     print(f'header:{header}')
#     cookie = login_oldadmin
#     print(f'cookie:{cookie}')
#     dtipinfo['nodeId'] = nodes_idSet
#     print(f'dtipinfo:{dtipinfo}')
#     s = common.Webrequests()
#     response = s.run_main(method, url, dtipinfo, header, cookie)
#     print(response)
#     assert response['status'] == expected
#     sleep(5)


if __name__ == "__main__":
    pytest.main(["test_wxt02_admininit&auth.py"])