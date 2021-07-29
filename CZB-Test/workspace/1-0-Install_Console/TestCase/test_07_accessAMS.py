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

@allure.title("接入AMS成功！")
@pytest.mark.parametrize("amsinfo, expected",
                         [
                             ({"port": 9781}, "success")
                         ])
def test_accessAMS(login_admin, get_baseurl, get_version, get_amsIPorDomain, amsinfo, expected):
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    method = res['ams_method']
    url = parse.urljoin(base_url, res['ams_url'])
    referer = parse.urljoin(base_url, res['ams_referer'])
    
    if get_amsIPorDomain == False:
        pytest.skip(msg='This test will not run when you do not want to connect the console to AMS')
    elif version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_admin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_admin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    amsinfo["ipOrDomain"] = get_amsIPorDomain

    s = common.Webrequests()
    response = s.run_main(method, url, amsinfo, header, cookie)
    print(response)
    assert response['status'] == expected

if __name__ == '___main__':
    pytest.main(["test_07_accessAMS.py --Console_URL=base_url --Version=version --AMSIPOrDomain=amsIPorDomain"])
