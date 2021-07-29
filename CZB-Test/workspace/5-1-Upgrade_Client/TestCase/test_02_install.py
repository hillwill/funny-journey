#!/usr/bin/env python
# *-*coding:utf-8*-*
import sys
sys.path.append("/eisoo/CZB-Test/workspace")
import pytest
import yaml
from common import common
from urllib import parse
import allure
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from time import sleep

@allure.title("添加主机配置成功！")
@pytest.mark.parametrize("hostinfo, expected",
                         [
                             ({"authType": 1,
                               "installParam": {"dbParam": []},
                               "installPath": "/opt",
                               "rootPwd": "",
                               "sshPort": 22,
                               "sshUser": "root"}, "success")
                         ])
def test_host_configuration(login_admin, get_clientip, get_clientdatabase, get_clientdatabasename, get_clientCDP, get_baseurl, get_version, get_clientpwd, get_clientusername, hostinfo, expected):
    # file = open("D:\\1-1-Install_Client\\TestData\\config.yaml", encoding='utf-8')
    file = open('/eisoo/CZB-Test/workspace/5-1-Upgrade_Client/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    method = res['host_method']
    url = parse.urljoin(base_url, res['host_url'])
    referer = parse.urljoin(base_url, res['host_referer'])

    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_admin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_admin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}

    hostinfo['localIp'] = get_clientip
    hostinfo['name'] = get_clientip
    hostinfo['sshIp'] = get_clientip
    hostinfo['sshPwd'] = get_clientpwd
    hostinfo['installParam']['enableCdp'] = get_clientCDP
    print(get_clientdatabase)
    if get_clientdatabase != 'None':
        hostinfo['installParam']['dbParam'] = [{"dbType": "%s" %(get_clientdatabase), "user": "%s" %(get_clientdatabasename)}]
    print(hostinfo)

    s = common.Webrequests()
    response = s.run_main(method, url, hostinfo, header, cookie)
    print(response)
    assert response['status'] == expected

@allure.title("添加部署计划成功！")
@pytest.mark.parametrize("planinfo, expected",
                         [
                             ({"desc": ""}, "success")
                         ])
def test_plan(login_admin, get_baseurl, get_version, get_host_idSet_from_ip, get_clientip, planinfo, expected):
    # file = open("D:\\1-1-Install_Client\\TestData\\config.yaml", encoding='utf-8')
    file = open('/eisoo/CZB-Test/workspace/5-1-Upgrade_Client/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    method = res['plan_method']
    url = parse.urljoin(base_url, res['plan_url'])
    referer = parse.urljoin(base_url, res['plan_referer'])

    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_admin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_admin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}

    planinfo['idList'] = ["%s" %(get_host_idSet_from_ip)]
    planinfo['name'] = get_clientip
    print(planinfo)

    s = common.Webrequests()
    response = s.run_main(method, url, planinfo, header, cookie)
    print(response)
    assert response['status'] == expected

@allure.title("启动部署计划成功！")
@pytest.mark.parametrize("installinfo, expected",
                         [
                             ({}, "success")
                         ])
def test_install(login_admin, get_baseurl, get_version, get_plan_idSet_from_name, installinfo, expected):
    # file = open("D:\\1-1-Install_Client\\TestData\\config.yaml", encoding='utf-8')
    file = open('/eisoo/CZB-Test/workspace/1-1-Install_Client/TestData/config.yaml')
    file = open('/eisoo/CZB-Test/workspace/5-1-Upgrade_Client/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    method = res['install_method']
    url = parse.urljoin(base_url, res['install_url'])
    referer = parse.urljoin(base_url, res['install_referer'])

    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_admin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_admin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}

    installinfo['planId'] = get_plan_idSet_from_name

    s = common.Webrequests()
    response = s.run_main(method, url, installinfo, header, cookie)
    print(response)
    assert response['status'] == expected
    sleep(100)

#@allure.title("查看客户端部署结果！")
#@pytest.mark.parametrize("overinfo, expected",
#                         [
#                             ({"index":0,
#                               "count": 15}, 32)
#                         ])
#def test_over(login_admin, get_baseurl, get_version, get_planname, overinfo, expected):
#    # file = open("D:\\1-1-Install_Client\\TestData\\config.yaml", encoding='utf-8')
#    file = open('/eisoo/CZB-Test/workspace/5-1-Upgrade_Client/TestData/config.yaml')
#    res = yaml.load(file, Loader=yaml.FullLoader)
#    base_url = get_baseurl
#    version = get_version
#
#    method = res['over_method']
#    url = parse.urljoin(base_url, res['over_url'])
#    referer = parse.urljoin(base_url, res['over_referer'])
#
#    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
#        cookie, userId = login_admin
#        header = {"referer": "%s" % (referer)}
#    else:
#        cookie, userId, csrftoken = login_admin
#        header = {"referer": "%s" % (referer),
#                  "x-csrftoken": "%s" % (csrftoken)}
#
#    s = common.Webrequests()
#    response = s.run_main(method, url, overinfo, header, cookie)
#    print(response)
#    
#    totalNum = response['responseData']['totalNum']
#    print(totalNum)
#    i = 0
#    while i < totalNum:
#        if response['responseData']['data'][i]['planName'] == get_planname:
#            assert response['responseData']['data'][i]['status'] == 32
#        else:
#            i += 1

@allure.title("删除部署计划成功！")
@pytest.mark.parametrize("planinfo, expected",
                         [
                             ({}, "success")
                         ])
def test_deleteplan(login_admin, get_baseurl, get_version, get_plan_idSet_from_name, planinfo, expected):
    # file = open("D:\\1-1-Install_Client\\TestData\\config.yaml", encoding='utf-8')
    file = open('/eisoo/CZB-Test/workspace/5-1-Upgrade_Client/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    method = res['deleteplan_method']
    url = parse.urljoin(base_url, res['deleteplan_url'])
    referer = parse.urljoin(base_url, res['deleteplan_referer'])

    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_admin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_admin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}

    planinfo['planId'] = ["%s" %(get_plan_idSet_from_name)]

    s = common.Webrequests()
    response = s.run_main(method, url, planinfo, header, cookie)
    print(response)
    assert response['status'] == expected

@allure.title("删除主机配置成功！")
@pytest.mark.parametrize("deletehostinfo, expected",
                         [
                             ({}, "success")
                         ])
def test_deletehost(login_admin, get_baseurl, get_version, get_host_idSet_from_ip, get_clientip, deletehostinfo, expected):
    # file = open("D:\\1-1-Install_Client\\TestData\\config.yaml", encoding='utf-8')
    file = open('/eisoo/CZB-Test/workspace/5-1-Upgrade_Client/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    method = res['deletehost_method']
    url = parse.urljoin(base_url, res['deletehost_url'])
    referer = parse.urljoin(base_url, res['deletehost_referer'])

    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_admin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_admin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}

    deletehostinfo['clientId'] = ["%s" %(get_host_idSet_from_ip)]
    print(deletehostinfo)

    s = common.Webrequests()
    response = s.run_main(method, url, deletehostinfo, header, cookie)
    print(response)
    assert response['status'] == expected

if __name__ == '___main__':
    pytest.main(["test_02_install.py --Console_URL=base_url --Version=version --Client_IP=clientip --Client_Usernmae=clientusername --Client_Pwd=clientpwd --Client_CDP=clientcdp --Client_Database=clientdatabase --Client_databaseName=cleintdatabasename"])
