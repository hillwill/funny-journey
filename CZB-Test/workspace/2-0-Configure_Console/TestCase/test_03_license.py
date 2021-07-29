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

@allure.title("导入授权码成功!")
def test_license(login_admin, get_baseurl, get_version):
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    url = parse.urljoin(base_url, res['license_url'])
    print(url)
    method = res['license_method']
    referer = parse.urljoin(base_url, res['license_referer'])

    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_admin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_admin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}

    files = {'file': open("License.dat", 'rb')}
    print(header)
    print(cookie)
    s = common.Webrequests()
    response = s.run_main(method, url, files, header, cookie)
    print(response)
    assert response['status'] == "success"

@allure.title("批量激活成功!")
def test_active(login_admin, get_baseurl, get_version):
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    url = parse.urljoin(base_url, res['active_url'])
    print(url)
    method = res['active_method']
    referer = parse.urljoin(base_url, res['active_referer'])

    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_admin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_admin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}

    files = {'file': open("Active.dat", 'rb')}
    print(header)
    print(cookie)
    s = common.Webrequests()
    response = s.run_main(method, url, files, header, cookie)
    print(response)
    assert response['status'] == "success"

if __name__ == '__main__':
    pytest.main('test_03_license.py --Console_URL=base_url --Version=version --License.dat=License.dat --Active.dat=Active.dat')
