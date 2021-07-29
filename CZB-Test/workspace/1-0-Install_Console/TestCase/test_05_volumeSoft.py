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

@allure.title("创建OFS卷成功！")
@pytest.mark.parametrize("ofsinfo, expected",
                         [
                             ({"desc": "",
                               "name": "OFS",
                               "ngDialogId": "ngdialog8",
                               "storageType": 0,
                               "type": 1}, "success"),
                         ])
def test_CreateOFS(login_admin, get_baseurl, get_version, path_catch, node_idSet_Soft, ofsinfo, expected, get_softvolumenodeIP):
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    method = res['volume_method']
    url = parse.urljoin(base_url, res['volume_url'])
    referer = parse.urljoin(base_url, res['volume_referer'])

    if get_softvolumenodeIP == False:
        pytest.skip(msg='This test is only for CentOS Console')
    elif version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_admin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_admin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    usablePath, freeSize = path_catch
    ofsinfo["nodeId"] = node_idSet_Soft
    ofsinfo['mountPath'] = usablePath
    ofsinfo['pathSize'] = freeSize
    size = int(freeSize / 1024 / 1024 / 1024 * 0.4) * 1024 * 1024 * 1024
    ofsinfo['size'] = size

    s = common.Webrequests()
    response = s.run_main(method, url, ofsinfo, header, cookie)
    print(response)
    assert response['status'] == expected

@allure.title("创建META卷成功！")
@pytest.mark.parametrize("metainfo, expected",
                         [
                             ({"desc": "",
                               "name": "META",
                               "ngDialogId": "ngdialog8",
                               "storageType": 0,
                               "type": 3}, "success"),
                         ])
def test_CreateMETA(login_admin, get_baseurl, get_version, path_catch, node_idSet_Soft, metainfo, expected, get_softvolumenodeIP):
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    method = res['volume_method']
    url = parse.urljoin(base_url, res['volume_url'])
    referer = parse.urljoin(base_url, res['volume_referer'])
    
    if get_softvolumenodeIP == False:
        pytest.skip(msg='This test is only for CentOS Console')
    elif version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_admin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_admin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    usablePath, freeSize = path_catch
    metainfo["nodeId"] = node_idSet_Soft
    metainfo['mountPath'] = usablePath
    metainfo['pathSize'] = freeSize
    size = int(freeSize / 1024 / 1024 / 1024 * 0.2) * 1024 * 1024 * 1024
    metainfo['size'] = size

    s = common.Webrequests()
    response = s.run_main(method, url, metainfo, header, cookie)
    print(response)
    assert response['status'] == expected

@allure.title("创建DDC卷成功！")
@pytest.mark.parametrize("ddcinfo, expected",
                         [
                             ({"desc": "",
                               "name": "DDC",
                               "ngDialogId": "ngdialog8",
                               "storageType": 0,
                               "type": 2}, "success"),
                         ])
def test_CreateDDC(login_admin, get_baseurl, get_version, path_catch, node_idSet_Soft, ddcinfo, expected, get_softvolumenodeIP):
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    method = res['volume_method']
    url = parse.urljoin(base_url, res['volume_url'])
    referer = parse.urljoin(base_url, res['volume_referer'])
    
    if get_softvolumenodeIP == False:
        pytest.skip(msg='This test is only for CentOS Console')
    elif version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_admin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_admin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    usablePath, freeSize = path_catch

    ddcinfo["nodeId"] = node_idSet_Soft
    ddcinfo['mountPath'] = usablePath
    ddcinfo['pathSize'] = freeSize
    size = 15 * 1024 * 1024 * 1024
    ddcinfo['size'] = size

    s = common.Webrequests()
    response = s.run_main(method, url, ddcinfo, header, cookie)
    print(response)
    assert response['status'] == expected
    sleep(60)

@allure.title("创建SELF卷成功！")
@pytest.mark.parametrize("selfinfo, expected",
                         [
                             ({"desc": "",
                               "name": "SELF",
                               "ngDialogId": "ngdialog8",
                               "storageType": 0,
                               "type": 5}, "success"),
                         ])
def test_CreateSELF(login_admin, get_baseurl, get_version, path_catch, node_idSet_Soft, selfinfo, expected, get_softvolumenodeIP):
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    method = res['volume_method']
    url = parse.urljoin(base_url, res['volume_url'])
    referer = parse.urljoin(base_url, res['volume_referer'])
    
    if get_softvolumenodeIP == False:
        pytest.skip(msg='This test is only for CentOS Console')
    elif version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_admin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_admin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    usablePath, freeSize = path_catch
    selfinfo["nodeId"] = node_idSet_Soft
    selfinfo['mountPath'] = usablePath
    selfinfo['pathSize'] = freeSize
    size = 20 * 1024 * 1024 * 1024
    selfinfo['size'] = size

    s = common.Webrequests()
    response = s.run_main(method, url, selfinfo, header, cookie)
    print(response)
    assert response['status'] == expected

if __name__== '___main__':
    pytest.main(["test_05_volumeSoft.py --Console_URL=base_url --Version=version --SoftVolumeNodeIP=softvolumenodeIP"])
