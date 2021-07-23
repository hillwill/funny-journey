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

@allure.title("初始化操作员成功!")
@pytest.mark.parametrize("initoperator, expected",
                         [
                             ({"isEnc": "true",
                               "oldUserPass": "DN5+zryo6mSfoOjYIYKD44PlWtjxaF5YkBZPWQ2XDiJ0zJaLboHnLzKA+nl9feKJjFgK5aGDURI4rHQpU2cfJSndi/ikG3HSD3vVC1z1v2G+0PF65iWEhfZ8Rm7JRDwyqBBnC8Tclzkm28APmApkR527So0SVY92ay4m/LCL7NI=",
                               "userPass": "LDm5VpovKEISErwLXkd4AheRJ/bQ4j87gqo/QjrOw7Exc0cZLN/+ii1lVwh1rX0zchhlGt85W/s+HF6+uZ5II6vZ8Q3wdaCcYTxXY/xwgiRZnLK4jGf4tyr5M5BTTnv0JYbCE+L4VZzynlxpmh8eloQYKX9/av3T0cp40xpsBdM=",
                               "repeatUserPass": "LDm5VpovKEISErwLXkd4AheRJ/bQ4j87gqo/QjrOw7Exc0cZLN/+ii1lVwh1rX0zchhlGt85W/s+HF6+uZ5II6vZ8Q3wdaCcYTxXY/xwgiRZnLK4jGf4tyr5M5BTTnv0JYbCE+L4VZzynlxpmh8eloQYKX9/av3T0cp40xpsBdM="}, "success"),
                         ])

def test_init_operator(login_newoperator, initoperator, expected, operator_idSet):
    file = open('D:\\MyProject\\Api-test\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['init_url']).format(operator_idSet)
    header = res['init_headers']
    method = res['init_method']
    cookie = login_newoperator
    userId = operator_idSet
    initoperator['userId'] = userId
    print(url, header, method, userId)
    initoperator['userId'] = userId
    s = common.Webrequests()
    response = s.run_main(method, url, initoperator, header, cookie)
    print(response)
    assert response['status'] == expected
    sleep(5)

# @allure.title("创建指纹库成功!")
# @pytest.mark.parametrize("flinfo, expected",
#                          [
#                              ({"appType": 0,
#                                "flName": "zwk1",
#                                "fpName": "zwc"}, "success"),
#                          ])
# def test_createfl(login_oldoperator, flinfo, expected, fp_idSet):
#     file = open('D:\\MyProject\\Api-test\\TestData\\config.yaml', encoding='utf-8')
#     res = yaml.load(file, Loader=yaml.FullLoader)
#     url = parse.urljoin(res['base_url'], res['fl_url'])
#     header = res['fl_headers']
#     method = res['fl_method']
#     cookie = login_oldoperator
#     fpGuid = fp_idSet
#     flinfo['fpGuid'] = fpGuid
#     print(url, header, method, fpGuid)
#     s = common.Webrequests()
#     response = s.run_main(method, url, flinfo, header, cookie)
#     print(response)
#     assert response['status'] == expected
#     sleep(5)

if __name__ == "__main__":
    pytest.main(["test_wxt06_wxtinit&auth.py"])