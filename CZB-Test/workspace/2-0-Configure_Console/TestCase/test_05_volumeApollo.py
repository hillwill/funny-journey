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

@allure.title("创建raid成功！")
@pytest.mark.parametrize("raidinfo, expected",
                         [
                             ({"raidLevel": 0,
                               "raidName": "md1",
                               "readCache": 1,
                               "stripSize": 262144,
                               "subDisk": "3",
                               "subGroup": 3,
                               "writeCache": 1}, "success"),
                         ])
def test_CreateRaid(login_admin, get_baseurl, get_version, disk_catch, node_idSet, raidinfo, expected, get_volumenodeIP, raid_YesorNo):
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    url = parse.urljoin(base_url, res['raid_url'])
    referer = parse.urljoin(base_url, res['raid_referer'])
    method = res['raid_method']
    print(f'raid_YesorNo:{raid_YesorNo}')

    if get_volumenodeIP == False:
        pytest.skip(msg='This test is only for Apollo Console')
    elif version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_admin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_admin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}

    if raid_YesorNo:
        # 若不存在raid则创建
        if disk_catch == False:
            print("无可用磁盘")
        else:
            diskId01 = disk_catch
            print(f'diskId01:{diskId01}')
            raidinfo["nodeId"] = node_idSet
            raidinfo["nodeIp"] = get_volumenodeIP
            raidinfo["disks"] = [{"devId": f'{diskId01}'}]
            s = common.Webrequests()
            print(raidinfo)
            response = s.run_main(method, url, raidinfo, header, cookie)
            print(response)
            response['status'] = expected
            sleep(60)

@allure.title("创建OFS卷成功！")
@pytest.mark.parametrize("ofsinfo, expected",
                         [
                             ({"desc": "",
                               "name": "OFS",
                               "ngDialogId": "ngdialog27",
                               "requestId": "",
                               "storageType": 1,
                               "type": 1}, "success"),
                         ])
def test_CreateOFS(login_admin, get_baseurl, get_version, raid_catch, node_idSet, ofsinfo, expected, get_volumenodeIP):
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    method = res['volume_method']
    url = parse.urljoin(base_url, res['volume_url'])
    referer = parse.urljoin(base_url, res['volume_referer'])
    
    if get_volumenodeIP == False:
        pytest.skip(msg='This test is only for Apollo Console')
    elif version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_admin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_admin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    raidSize, raidUsable, raidName, raidType = raid_catch
    ofsinfo['raidTotal'] = raidSize
    ofsinfo['raidUsable'] = raidUsable
    ofsinfo["nodeId"] = node_idSet
    ofsinfo['raidName'] = raidName
    ofsinfo['raidType'] = raidType
    size = 100 * 1024 * 1024 * 1024
    ofsinfo['size'] = size
    print(get_volumenodeIP)
    print(ofsinfo)

    s = common.Webrequests()
    response = s.run_main(method, url, ofsinfo, header, cookie)
    print(response)
    assert response['status'] == expected

@allure.title("创建META卷成功！")
@pytest.mark.parametrize("metainfo, expected",
                         [
                             ({"desc": "",
                               "name": "META",
                               "ngDialogId": "ngdialog27",
                               "requestId": "",
                               "storageType": 1,
                               "type": 3}, "success"),
                         ])
def test_CreateMETA(login_admin, get_baseurl, get_version, raid_catch, node_idSet, metainfo, expected, get_volumenodeIP):
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    method = res['volume_method']
    url = parse.urljoin(base_url, res['volume_url'])
    referer = parse.urljoin(base_url, res['volume_referer'])
    
    if get_volumenodeIP == False:
        pytest.skip(msg='This test is only for Apollo Console')
    elif version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_admin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_admin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    raidSize, raidUsable, raidName, raidType = raid_catch
    metainfo['raidTotal'] = raidSize
    metainfo['raidUsable'] = raidUsable
    metainfo["nodeId"] = node_idSet
    metainfo['raidName'] = raidName
    metainfo['raidType'] = raidType
    size = 10 * 1024 * 1024 * 1024
    metainfo['size'] = size
    print(get_volumenodeIP)
    print(metainfo)

    s = common.Webrequests()
    response = s.run_main(method, url, metainfo, header, cookie)
    print(response)
    assert response['status'] == expected

@allure.title("创建DDC卷成功！")
@pytest.mark.parametrize("ddcinfo, expected",
                         [
                             ({"desc": "",
                               "name": "DDC",
                               "ngDialogId": "ngdialog27",
                               "requestId": "",
                               "storageType": 1,
                               "type": 2}, "success"),
                         ])
def test_CreateDDC(login_admin, get_baseurl, get_version, raid_catch, node_idSet, ddcinfo, expected, get_volumenodeIP):
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    method = res['volume_method']
    url = parse.urljoin(base_url, res['volume_url'])
    referer = parse.urljoin(base_url, res['volume_referer'])
    
    if get_volumenodeIP == False:
        pytest.skip(msg='This test is only for Apollo Console')
    elif version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_admin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_admin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    raidSize, raidUsable, raidName, raidType = raid_catch
    ddcinfo['raidTotal'] = raidSize
    ddcinfo['raidUsable'] = raidUsable
    ddcinfo["nodeId"] = node_idSet
    ddcinfo['raidName'] = raidName
    ddcinfo['raidType'] = raidType
    size = 10 * 1024 * 1024 * 1024
    ddcinfo['size'] = size
    print(get_volumenodeIP)
    print(ddcinfo)
    print(url)
    print(header)
    print(cookie)

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
                               "ngDialogId": "ngdialog27",
                               "requestId": "",
                               "storageType": 1,
                               "type": 5}, "success"),
                         ])
def test_CreateSELF(login_admin, get_baseurl, get_version, raid_catch, node_idSet, selfinfo, expected, get_volumenodeIP):
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    method = res['volume_method']
    url = parse.urljoin(base_url, res['volume_url'])
    referer = parse.urljoin(base_url, res['volume_referer'])

    if get_volumenodeIP == False:
        pytest.skip(msg='This test is only for Apollo Console')
    elif version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_admin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_admin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    raidSize, raidUsable, raidName, raidType = raid_catch
    selfinfo['raidTotal'] = raidSize
    selfinfo['raidUsable'] = raidUsable
    selfinfo["nodeId"] = node_idSet
    selfinfo['raidName'] = raidName
    selfinfo['raidType'] = raidType
    size = 20 * 1024 * 1024 * 1024
    selfinfo['size'] = size
    print(get_volumenodeIP)
    print(selfinfo)

    s = common.Webrequests()
    response = s.run_main(method, url, selfinfo, header, cookie)
    print(response)
    assert response['status'] == expected


if __name__== '___main__':
    pytest.main(["test_05_volumeApollo.py --Console_URL=base_url --Version=version --VolumeNodeIP=volumenodeIP"])
