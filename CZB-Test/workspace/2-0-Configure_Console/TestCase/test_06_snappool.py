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
from time import sleep
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

@allure.title("创建存储池成功！")
@pytest.mark.parametrize("poolinfo, expected",
                         [
                             ({"poolId": "false",
                               "poolName": "存储池",
                               "safeThreshold": 95,
                               "size": 1024,
                               "warnThreshold": 90}, "success"),
                         ])
def test_CreatePool(login_admin, get_baseurl, get_version, mdisks_catch, node_idSet_pool, poolinfo, expected, get_snappoolnodeIP):
    if mdisks_catch != None:
        file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
        # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
        res = yaml.load(file, Loader=yaml.FullLoader)
        base_url = get_baseurl
        version = get_version
        method = res['snappool_method']
        url = parse.urljoin(base_url, res['snappool_url'])
        referer = parse.urljoin(base_url, res['snappool_referer'])
        print(mdisks_catch)
        print(get_snappoolnodeIP)

        if get_snappoolnodeIP == False:
            pytest.skip(msg='This test will not run when you do not want to create s snappool')
        elif version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
            cookie, userId = login_admin
            header = {"referer": "%s" % (referer)}
        else:
            cookie, userId, csrftoken = login_admin
            header = {"referer": "%s" % (referer),
                      "x-csrftoken": "%s" % (csrftoken)}
        diskId = mdisks_catch
        poolinfo["deviceId"] = node_idSet_pool
        poolinfo['mDisks'] = ["%s" %diskId]

        s = common.Webrequests()
        response = s.run_main(method, url, poolinfo, header, cookie)
        print(response)
        assert response['status'] == expected
    else:
        assert "success" == "success"

if __name__== '___main__':
    pytest.main(["test_06_snappool.py --Console_URL=base_url --Version=version --SnapPoolNodeIP=snappoolnodeIP"])
