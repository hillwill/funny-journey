#!/usr/bin/env python
#*-*coding:utf-8*-*
import sys
sys.path.append("/eisoo/CZB-Test/workspace/")
import yaml
import pytest
import allure
from urllib import parse
from common import common
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

@allure.title("初始化admin成功！")
@pytest.mark.parametrize("initadmin, expected",
                         [
                             ({"isEnc": "true",
                               "oldUserPass": "SCLoaaS+9Q3zrFzyOobMYWB+3Q8MWJFVcTlO6e0bzBR2IlTxXHbtYHpQzqXZ9/eDMEEQdat3DSEOaIPDFCz0drPZEczi6ZJfKF9EambRNa36eEttwwXisw9yh5vd9J3odn2TcT0GF8kkLHnIG0L59+MuFLcCwfMBAGXquyEvUc0=",
                               "repeatUserPass": "esYlYQc8VB6JeM7WwZxdtaeDwxI2nUu8/cF84xwKx56kq9gxkZsIlMaq36uE54mhbbvg4PzKL7npG2MDo9FEf5FxLVHohKOVIpzq3dGsapE7WlYdXj4YECrV84Fdcbxtk0nmd+HpTcjU3Q2jovYqGbnRvD2Vw3xNmgWP1cFHHb4=",
                               "userPass": "jKoXRkEAsMBThpvCXCqVOQm4ExesYLjGxgLuWNNwlKeYNOJPoR3yGZkNiANVVcmzVgHdr1ow9AF0rA4zEIhqmKZRMphYJpQfJTL2cm+qXfVFEM/5UjDG4cPTiIm7gejixaBZraRZEAQ820uSmVi/etg0bZvsCsUtSsQsmajgsMI="}, "success"),
                         ])
def test_init_admin(login_Initialadmin, get_baseurl, get_version, initadmin, expected):
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    file = open('/eisoo/CZB-Test/workspace/1-1-Install_Client/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)

    # 获取Console_URL, Version参数的值
    base_url = get_baseurl
    version = get_version

    # 通过拼接得到请求的各项参数
    method = res['init_method']
    referer = parse.urljoin(base_url, res['init_referer'])

    if login_Initialadmin == False:
        # 如果admin已初始化完成，则跳过这条用例
        pytest.skip(msg='admin has been initialized')
    elif version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_Initialadmin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_Initialadmin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}

    initadmin['userId'] = userId
    url = parse.urljoin(base_url, res['init_url']).format(userId)

    # 通过requests发送请求，验证返回值
    s = common.Webrequests()
    admin_init_response = s.run_main(method, url, initadmin, header, cookie)
    assert admin_init_response['status'] == expected

@allure.title("初始化sadmin成功！")
@pytest.mark.parametrize("initsadmin, expected",
                         [
                             ({"isEnc": "true",
                               "oldUserPass": "SCLoaaS+9Q3zrFzyOobMYWB+3Q8MWJFVcTlO6e0bzBR2IlTxXHbtYHpQzqXZ9/eDMEEQdat3DSEOaIPDFCz0drPZEczi6ZJfKF9EambRNa36eEttwwXisw9yh5vd9J3odn2TcT0GF8kkLHnIG0L59+MuFLcCwfMBAGXquyEvUc0=",
                               "repeatUserPass": "esYlYQc8VB6JeM7WwZxdtaeDwxI2nUu8/cF84xwKx56kq9gxkZsIlMaq36uE54mhbbvg4PzKL7npG2MDo9FEf5FxLVHohKOVIpzq3dGsapE7WlYdXj4YECrV84Fdcbxtk0nmd+HpTcjU3Q2jovYqGbnRvD2Vw3xNmgWP1cFHHb4=",
                               "userPass": "jKoXRkEAsMBThpvCXCqVOQm4ExesYLjGxgLuWNNwlKeYNOJPoR3yGZkNiANVVcmzVgHdr1ow9AF0rA4zEIhqmKZRMphYJpQfJTL2cm+qXfVFEM/5UjDG4cPTiIm7gejixaBZraRZEAQ820uSmVi/etg0bZvsCsUtSsQsmajgsMI="}, "success"),
                         ])
def test_init_sadmin(login_Initialsadmin, get_baseurl, get_version, initsadmin, expected):
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    file = open('/eisoo/CZB-Test/workspace/1-1-Install_Client/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)

    # 获取Console_URL, Version参数的值
    base_url = get_baseurl
    version = get_version

    # 通过拼接得到请求的各项参数
    method = res['init_method']
    referer = parse.urljoin(base_url, res['init_referer'])

    if login_Initialsadmin == False:
        # 如果sadmin已初始化完成，则跳过这条用例
        pytest.skip(msg='sadmin has been initialized')
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_Initialsadmin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_Initialsadmin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}

    initsadmin['userId'] = userId
    url = parse.urljoin(base_url, res['init_url']).format(userId)

    # 通过requests发送请求，验证返回值
    s = common.Webrequests()
    sadmin_init_response = s.run_main(method, url, initsadmin, header, cookie)
    assert sadmin_init_response['status'] == expected

if __name__== '___main__':
    pytest.main(["test_01_init.py --Console_URL=base_url --Version=version"])
