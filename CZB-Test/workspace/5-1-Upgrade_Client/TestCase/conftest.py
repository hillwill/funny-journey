#!/usr/bin/env python
# *-*coding:utf-8*-*
import sys
sys.path.append("D:\\1-1-Install_Client")
import pytest
import yaml
from urllib import parse
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def pytest_addoption(parser):
    """新增运行参数--Console_URL, Version, VolumeNodeIP"""
    parser.addoption(
        "--Console_URL", action="store", default=""
    )
    parser.addoption(
        "--Version", action="store", default=""
    )
    parser.addoption(
        "--Client_IP", action="store", default=""
    )
    parser.addoption(
        "--Client_Username", action="store", default=""
    )
    parser.addoption(
        "--Client_Pwd", action="store", default=""
    )
    parser.addoption(
        "--Client_CDP", action="store", default=""
    )
    parser.addoption(
        "--Client_Database", action="store", default="None"
    )
    parser.addoption(
        "--Client_databaseName", action="store", default="False"
    )

@pytest.fixture()  #获取Console_URL
def get_baseurl(pytestconfig):
    print(pytestconfig.getoption('--Console_URL'))
    return pytestconfig.getoption('--Console_URL')

@pytest.fixture()  #获取版本信息
def get_version(pytestconfig):
    print(pytestconfig.getoption('--Version'))
    return pytestconfig.getoption('--Version')

@pytest.fixture()  #获取客户端IP
def get_clientip(pytestconfig):
    print(pytestconfig.getoption('--Client_IP'))
    return pytestconfig.getoption('--Client_IP')

@pytest.fixture()  #获取客户端Username
def get_clientusername(pytestconfig):
    print(pytestconfig.getoption('--Client_Username'))
    return pytestconfig.getoption('--Client_Username')

@pytest.fixture()  #获取客户端ssh密码
def get_clientpwd(pytestconfig):
    print(pytestconfig.getoption('--Client_Pwd'))
    return pytestconfig.getoption('--Client_Pwd')

@pytest.fixture()  #获取客户端CDP配置
def get_clientCDP(pytestconfig):
    print(pytestconfig.getoption('--Client_CDP'))
    return pytestconfig.getoption('--Client_CDP')

@pytest.fixture()  #获取客户端数据库配置
def get_clientdatabase(pytestconfig):
    print(pytestconfig.getoption('--Client_Database'))
    return pytestconfig.getoption('--Client_Database')

@pytest.fixture()  #获取客户端CDP配置
def get_clientdatabasename(pytestconfig):
    print(pytestconfig.getoption('--Client_databaseName'))
    return pytestconfig.getoption('--Client_databaseName')

@pytest.fixture()
def login_admin(get_baseurl, get_version):
    """获取已初始化的admin用户的cookie"""
    # file = open("D:\\1-1-Install_Client\\TestData\\config.yaml", encoding='utf-8')
    file = open('/eisoo/CZB-Test/workspace/5-1-Upgrade_Client/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    print(version)

    url = parse.urljoin(base_url, res['login_url'])
    referer = parse.urljoin(base_url, res['login_referer'])
    header = {'referer': '%s' %(referer)}
    datainfo = {"userName": "admin",
                "userPass": "DdiclnSMWi8n20cXSCiQbj0UOZpMUl8zxcf01fBv1LXzS4VVGanOkbhqhpgXzVys7yVLjpzUr3S/OqVoaUUP/MzVIOUtOB9J1dIa//zW6S0pumm/Ybnqmd+erN7Kj2MUfSnR/adhmu6DPCFmkYZM1lA6rIWKx5oiTX5imHFNJ3M=",  # eisoo.com123
                "validPwdExpire": "true",
                "isEnc": "true"}
    admin_login_response = requests.post(url, headers=header, json=datainfo, verify=False)
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie = admin_login_response.cookies
        userId = admin_login_response.cookies['userId']
        return cookie, userId
    else:
        cookie = admin_login_response.cookies
        userId = admin_login_response.cookies['userId']
        csrftoken = admin_login_response.cookies['csrftoken']
        return cookie, userId, csrftoken

@pytest.fixture()
def get_host_idSet_from_ip(get_baseurl, get_version, login_admin, get_clientip):
    """获取主机的的idList"""
    # file = open("D:\\1-1-Install_Client\\TestData\\config.yaml", encoding='utf-8')
    file = open('/eisoo/CZB-Test/workspace/5-1-Upgrade_Client/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    print(version)

    url = parse.urljoin(base_url, res['host_idSet_url'])
    referer = parse.urljoin(base_url, res['host_idSet_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_admin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_admin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    datainfo = {"count": 15,
                "index": 0}
    print(url)
    print(header)
    host_idSet_response = requests.get(url, headers=header, params=datainfo, verify=False, cookies=cookie).json()
    print(host_idSet_response)
    
    totalNum = host_idSet_response['responseData']['totalNum']
    i = 0
    while i < totalNum:
        if host_idSet_response['responseData']['data'][i]['localIp'] == get_clientip:
            return host_idSet_response['responseData']['data'][i]['clientId']
        else:
            i += 1

@pytest.fixture()
def get_plan_idSet_from_name(get_baseurl, get_version, login_admin, get_clientip):
    """获取部署计划的的planid"""
    # file = open("D:\\1-1-Install_Client\\TestData\\config.yaml", encoding='utf-8')
    file = open('/eisoo/CZB-Test/workspace/5-1-Upgrade_Client/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    print(version)

    url = parse.urljoin(base_url, res['plan_idSet_url'])
    referer = parse.urljoin(base_url, res['plan_idSet_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_admin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_admin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    datainfo = {"count": 15,
                "index": 0}
    print(url)
    print(header)
    plan_idSet_response = requests.get(url, headers=header, params=datainfo, verify=False, cookies=cookie).json()
    print(plan_idSet_response)
    
    totalNum = plan_idSet_response['responseData']['totalNum']
    i = 0
    while i < totalNum:
        if plan_idSet_response['responseData']['data'][i]['name'] == get_clientip:
            return plan_idSet_response['responseData']['data'][i]['planId']
        else:
            i += 1
