#!/usr/bin/env python
# *-*coding:utf-8*-*
import sys
# sys.path.append("D:\\2-1-Configure_Console")
sys.path.append("/eisoo/CZB-Test/workspace/")
import yaml
import pytest
import allure
from urllib import parse
from common import common
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

@allure.title("新建租户test成功！")
@pytest.mark.parametrize("opeinfo, expected",
                         [
                             ({"roleType": 5,
                               "userName": "test"}, "success")
                         ])
def test_newOperator(login_admin, get_baseurl, get_version, opeinfo, expected):
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)

    # 获取Console_URL, Version参数的值
    base_url = get_baseurl
    version = get_version

    # 通过拼接得到请求的各项参数
    method = res['operator_method']
    referer = parse.urljoin(base_url, res['operator_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_admin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_admin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    url = parse.urljoin(base_url, res['operator_url'])

    s = common.Webrequests()
    response = s.run_main(method, url, opeinfo, header, cookie)
    assert response['status'] == expected

@allure.title("初始化租户成功！")
@pytest.mark.parametrize("initoperator, expected",
                         [
                             ({"isEnc": "true",
                               "oldUserPass": "SCLoaaS+9Q3zrFzyOobMYWB+3Q8MWJFVcTlO6e0bzBR2IlTxXHbtYHpQzqXZ9/eDMEEQdat3DSEOaIPDFCz0drPZEczi6ZJfKF9EambRNa36eEttwwXisw9yh5vd9J3odn2TcT0GF8kkLHnIG0L59+MuFLcCwfMBAGXquyEvUc0=",
                               "repeatUserPass": "esYlYQc8VB6JeM7WwZxdtaeDwxI2nUu8/cF84xwKx56kq9gxkZsIlMaq36uE54mhbbvg4PzKL7npG2MDo9FEf5FxLVHohKOVIpzq3dGsapE7WlYdXj4YECrV84Fdcbxtk0nmd+HpTcjU3Q2jovYqGbnRvD2Vw3xNmgWP1cFHHb4=",
                               "userPass": "jKoXRkEAsMBThpvCXCqVOQm4ExesYLjGxgLuWNNwlKeYNOJPoR3yGZkNiANVVcmzVgHdr1ow9AF0rA4zEIhqmKZRMphYJpQfJTL2cm+qXfVFEM/5UjDG4cPTiIm7gejixaBZraRZEAQ820uSmVi/etg0bZvsCsUtSsQsmajgsMI="}, "success"),
                         ])
def test_init_sadmin(login_Initialoperator, get_baseurl, get_version, initoperator, expected):
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)

    # 获取Console_URL, Version参数的值
    base_url = get_baseurl
    version = get_version

    # 通过拼接得到请求的各项参数
    method = res['init_method']
    referer = parse.urljoin(base_url, res['init_referer'])

    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_Initialoperator
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_Initialoperator
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}

    initoperator['userId'] = userId
    url = parse.urljoin(base_url, res['init_url']).format(userId)

    # 通过requests发送请求，验证返回值
    s = common.Webrequests()
    sadmin_init_response = s.run_main(method, url, initoperator, header, cookie)
    assert sadmin_init_response['status'] == expected

if __name__ == '__main__':
    pytest.main('test_02_operator.py --Console_URL=base_url --Version=version')
