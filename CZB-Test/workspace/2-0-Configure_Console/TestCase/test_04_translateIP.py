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

@allure.title("添加备份数据传输IP成功！")
@pytest.mark.parametrize("transIP, expected",
                         [
                             ({}, "success"),
                         ])
def test_tranIP(login_admin, get_baseurl, get_version, nodes_idSet, transIP, expected):
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    url = parse.urljoin(base_url, res['transIP_url'])
    referer = parse.urljoin(base_url, res['transIP_referer'])
    method = res['transIP_method']

    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_admin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_admin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}

    nodes_ip, nodes_id = nodes_idSet
    i = 0
    for i in range(len(nodes_ip)):
        transIP["ipList"] = [("%s" %(nodes_ip[i]))]
        transIP["nodeId"] = ("%s" %(nodes_id[i]))
        print(transIP)
        s = common.Webrequests()
        response = s.run_main(method, url, transIP, header, cookie)
        print(response)
        assert response['status'] == expected

if __name__== '___main__':
    pytest.main(["test_04_translate.py --Console_URL=base_url --Version=version"])
