import sys
sys.path.append("/eisoo/CZB-Test/workspace/")
import pytest
import yaml
from urllib import parse
import requests
from time import sleep
import time
import datetime
import paramiko
from common import common
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# conftest.py说明：
# 1、注册命令行选项如下：
# Console_URL Version file_ClientIP file_ClientPwd file_DataSource oracle_ClientIP oracle_DatabaseName oracle_AuthUserName oracle_AuthPassword vmware_IP vmware_UserName vmware_Password vmware_DataSource
# 2、定义fixture函数如下:
# login_sadmin
# login_operator
# fp_nodeIps
# fp_Guid
# get_groupId
# get_filemd5
# platform_details_from_IP
# vmwarepath_from_uuid
# get_filedispath
# get_BuiltIn_Client_Id
# platform_verify
# get_oraclecustomer
# get_oracle_user
# get_timestamp

def pytest_addoption(parser):
    """新增运行参数--Console_URL, Version, VolumeNodeIP"""
    parser.addoption(
        "--Console_URL", action="store", default=""
    )
    parser.addoption(
        "--Version", action="store", default=""
    )
    parser.addoption(
        "--file_ClientIP", action="store", default="False"
    )
    parser.addoption(
        "--file_DataSource", action="store", default=""
    )
    parser.addoption(
        "--oracle_ClientIP", action="store", default="False"
    )
    parser.addoption(
        "--oracle_DatabaseName", action="store", default=""
    )
    parser.addoption(
        "--oracle_AuthUserName", action="store", default=""
    )
    parser.addoption(
        "--oracle_AuthPassword", action="store", default=""
    )
    parser.addoption(
        "--vmware_IP", action="store", default="False"
    )
    parser.addoption(
        "--vmware_Username", action="store", default=""
    )
    parser.addoption(
        "--vmware_Password", action="store", default=""
    )
    parser.addoption(
        "--vmware_DataSource", action="store", default=""
    )

@pytest.fixture()  #获取Console_URL
def get_baseurl(pytestconfig):
    print(pytestconfig.getoption('--Console_URL'))
    return pytestconfig.getoption('--Console_URL')

@pytest.fixture()  #获取控制台版本
def get_version(pytestconfig):
    print(pytestconfig.getoption('--Version'))
    Version = pytestconfig.getoption('--Version')
    return Version

@pytest.fixture()  #获取文件备份任务客户端IP
def get_clientip(pytestconfig):
    print(pytestconfig.getoption('--file_ClientIP'))
    file_ClientIP = pytestconfig.getoption('--file_ClientIP')
    if file_ClientIP == '':
        return False
    else:
        return file_ClientIP

@pytest.fixture()  #获取文件备份任务备份路径
def get_fullpath(pytestconfig):
    print(pytestconfig.getoption('--file_DataSource'))
    file_DataSource = pytestconfig.getoption('--file_DataSource')
    return file_DataSource

@pytest.fixture()   #获取oracle任务的客户端IP
def get_oracleclientip(pytestconfig):
    print(pytestconfig.getoption('--oracle_ClientIP'))
    oracle_ClientIP = pytestconfig.getoption('--oracle_ClientIP')
    if oracle_ClientIP == '':
        return False
    else:
        return oracle_ClientIP

@pytest.fixture()   #获取oracle的数据库名
def get_oracleDatabaseName(pytestconfig):
    oracle_DatabaseName = pytestconfig.getoption('--oracle_DatabaseName')
    return oracle_DatabaseName

@pytest.fixture()    #获取oracle的授权用户名
def get_oracleAuthUserName(pytestconfig):
    oracle_AuthUserName = pytestconfig.getoption('--oracle_AuthUserName')
    return oracle_AuthUserName

@pytest.fixture()   #获取oacle的授权密码
def get_oracleAuthPassword(pytestconfig):
    oracle_AuthPassword = pytestconfig.getoption('--oracle_AuthPassword')
    return oracle_AuthPassword

@pytest.fixture()  #获取VMware任务的平台IP
def get_vmwareip(pytestconfig):
    print(pytestconfig.getoption('--vmware_IP'))
    vmware_IP = pytestconfig.getoption('--vmware_IP')
    if vmware_IP == '':
        return False
    else:
        return vmware_IP

@pytest.fixture()  #获取VMware平台用户名
def get_vmwareusername(pytestconfig):
    print(pytestconfig.getoption('--vmware_Username'))
    return pytestconfig.getoption('--vmware_Username')

@pytest.fixture()  #获取VMware平台密码
def get_vmwarepassword(pytestconfig):
    print(pytestconfig.getoption('--vmware_Password'))
    return pytestconfig.getoption('--vmware_Password')

@pytest.fixture()  #获取VMware任务的数据源
def get_vmwaredatasource(pytestconfig):
    print(pytestconfig.getoption('--vmware_DataSource'))
    return pytestconfig.getoption('--vmware_DataSource')

@pytest.fixture()
def login_sadmin(get_baseurl, get_version):
    """获取sadmin用户的cookie"""
    file = open('/eisoo/CZB-Test/workspace/4-0-Prepare_Job/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    print(version)

    url = parse.urljoin(base_url, res['login_url'])
    referer = parse.urljoin(base_url, res['login_referer'])
    header = {'referer': '%s' %(referer)}
    datainfo = {"userName": "sadmin",
                "userPass": "DdiclnSMWi8n20cXSCiQbj0UOZpMUl8zxcf01fBv1LXzS4VVGanOkbhqhpgXzVys7yVLjpzUr3S/OqVoaUUP/MzVIOUtOB9J1dIa//zW6S0pumm/Ybnqmd+erN7Kj2MUfSnR/adhmu6DPCFmkYZM1lA6rIWKx5oiTX5imHFNJ3M=",  # eisoo.com123
                "validPwdExpire": "true",
                "isEnc": "true"}
    sadmin_login_response = requests.post(url, headers=header, json=datainfo, verify=False)
    print(sadmin_login_response)
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie = sadmin_login_response.cookies
        return cookie
    else:
        cookie = sadmin_login_response.cookies
        csrftoken = sadmin_login_response.cookies['csrftoken']
        return cookie, csrftoken

@pytest.fixture()
def get_filemd5(get_clientip, get_fullpath, get_clientpwd):
    """获取文件备份任务数据源的md5值"""
    ip = get_clientip
    port = 22
    password = get_clientpwd
    fullpath = get_fullpath
    print(fullpath)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=ip,
                    port=port,
                    username='root',
                    password=password,
                    timeout=60)
        print('控制台连接成功!')
    except Exception as e:
        print('控制台连接错误!', e)

    try:
        stdin, stdout, stderr = ssh.exec_command('find %s -type f -print0 | xargs -0 md5sum > /var/log/md5.log' %(fullpath))
        print('find %s -type f -print0 | xargs -0 md5sum > /var/log/md5.log' %(fullpath))
        print(stdout.read().decode('utf-8'))
        print('md5值计算完成:%s'%ip)
    except Exception as e:
        print('md5值计算错误:%s' %ip, e)

@pytest.fixture()
def login_operator(get_baseurl, get_version):
    """获取操作员用户的cookie"""
    file = open('/eisoo/CZB-Test/workspace/4-0-Prepare_Job/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    url = parse.urljoin(base_url, res['login_url'])
    referer = parse.urljoin(base_url, res['login_referer'])
    header = {'referer': '%s' %(referer)}
    datainfo = {"userName": "test",
                "userPass": "DdiclnSMWi8n20cXSCiQbj0UOZpMUl8zxcf01fBv1LXzS4VVGanOkbhqhpgXzVys7yVLjpzUr3S/OqVoaUUP/MzVIOUtOB9J1dIa//zW6S0pumm/Ybnqmd+erN7Kj2MUfSnR/adhmu6DPCFmkYZM1lA6rIWKx5oiTX5imHFNJ3M=",  # eisoo.com123
                "validPwdExpire": "true",
                "isEnc": "true"}
    test_login_response = requests.post(url, headers=header, json=datainfo, verify=False)

    if version in ('7.0.8.0','7.0.9.1','7.0.10.0','7.0.11.0'):
        cookie = test_login_response.cookies
        userId = test_login_response.cookies['userId']
        return cookie, userId
    else:
        cookie = test_login_response.cookies
        userId = test_login_response.cookies['userId']
        csrftoken = test_login_response.cookies['csrftoken']
        return cookie, userId, csrftoken

@pytest.fixture()
def fp_nodeIps(get_baseurl, get_version, login_operator):
    """获取控制台所有客户端的id列表"""
    file = open('/eisoo/CZB-Test/workspace/4-0-Prepare_Job/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    url = parse.urljoin(base_url, res['fp_nodeips_url'])
    referer = parse.urljoin(base_url, res['fp_nodeips_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie,userId = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_operator
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    datainfo = {"count": 5,
                "index": 0}
    print(url)
    print(referer)
    print(cookie)
    print(datainfo)

    fp_nodeIps_response = requests.get(url, params=datainfo, headers=header, verify=False, cookies=cookie).json()
    print(fp_nodeIps_response)
    totalNum = fp_nodeIps_response['responseData']['totalNum']
    i = 0
    fp_nodeIps = []
    while i < totalNum:
        fp_nodeIps.append(fp_nodeIps_response['responseData']['data'][i]['nodeIp'])
        i += 1
    return fp_nodeIps

@pytest.fixture()
def fp_Guid(get_baseurl, get_version, login_operator):
    """获取控制台上的指纹池id"""
    file = open('/eisoo/CZB-Test/workspace/4-0-Prepare_Job/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    url = parse.urljoin(base_url, res['fp_Guid_url'])
    referer = parse.urljoin(base_url, res['fp_Guid_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_operator
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    datainfo = {"count": 15,
                "index": 0}

    fp_Guid_response = requests.get(url, params=datainfo, headers=header, verify=False, cookies=cookie).json()
    print(fp_Guid_response)
    fpId = fp_Guid_response['responseData']['data'][0]['fpId']
    fpName = fp_Guid_response['responseData']['data'][0]['fpName']
    return fpId, fpName

@pytest.fixture()
def get_groupId(get_baseurl, get_version, login_operator):
    """获取客户端资源中默认组的id"""
    file = open('/eisoo/CZB-Test/workspace/4-0-Prepare_Job/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    url = parse.urljoin(base_url, res['groupId_url'])
    referer = parse.urljoin(base_url, res['groupId_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_operator
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    datainfo = {"count": 50,
                "index": 0}

    groupId_response = requests.get(url, params=datainfo, headers=header, verify=False, cookies=cookie).json()
    print(groupId_response)
    totalNum = groupId_response['responseData']['totalNum']
    i = 0
    while 1 < totalNum:
        if groupId_response['responseData']['data'][i]['groupType'] == 'default':
            groupId = groupId_response['responseData']['data'][i]['groupId']
            return groupId
        i += 1

@pytest.fixture()
def platform_details_from_IP(get_baseurl, get_version, login_operator, get_vmwareip):
    """获取VMware平台的具体信息"""
    file = open('/eisoo/CZB-Test/workspace/4-0-Prepare_Job/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    url = parse.urljoin(base_url, res['vmware_idSet_url'])
    referer = parse.urljoin(base_url, res['vmware_idSet_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_operator
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    datainfo = {"containsBuildin": 1,
                "count": 15,
                "filter": "",
                "index": 0,
                "isDistribute": 0}
    #print(f'platform_details_from_IP_url:{url}')
    #print(f'platform_details_from_ip_header:{header}')
    #print(f'platform_details_from_IP_datainfo:{datainfo}')

    platform_details_response = requests.get(url, params=datainfo, headers=header, verify=False, cookies=cookie).json()
    #print(platform_details_response)
    totalNum = platform_details_response['responseData']['totalNum']
    #print(totalNum)
    i = 0
    while i < totalNum:
        if platform_details_response['responseData']['data'][i]['ip'] == get_vmwareip:
            jobVplatformIP = platform_details_response['responseData']['data'][i]['ip']
            jobVplatformName = platform_details_response['responseData']['data'][i]['name']
            jobVplatformId = platform_details_response['responseData']['data'][i]['id']
            version = platform_details_response['responseData']['data'][i]['version']
            #print(jobVplatformIP)
            #print(jobVplatformName)
            #print(jobVplatformId)
            #print(version)
            return jobVplatformIP, jobVplatformName, jobVplatformId, version
        else:
            i += 1
            print(i)

@pytest.fixture()
def vmwarepath_from_search(get_baseurl, get_version, login_operator, platform_details_from_IP, get_vmwaredatasource, get_Builtin_Client_Id):
    """获取vmware备份数据源的fullpath,dispath"""
    file = open('/eisoo/CZB-Test/workspace/4-0-Prepare_Job/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    jobVplatformIP, jobVplatformName, jobVplatformId, version = platform_details_from_IP
    builtin_client_Id = get_Builtin_Client_Id
    timestamp = get_timestamp

    url = parse.urljoin(base_url, res['datasource_search_url']).format(builtin_client_Id)
    referer = parse.urljoin(base_url, res['datasource_search_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_operator
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    datainfo = {"code": "",
                "count": 150,
                "customer": "{\"mode\":\"host\",\"searchkey\":\"FTP\"}",
                "fullPath": "%s" %jobVplatformIP,
                "index": 0,
                "jobType": "eso_backupengine_vmwareengine",
                "partialSign": 0,
                "requestId": "",
                "type": 12000,
                "vplatformId": "%s" %jobVplatformId}
    print(f'url:{url}')
    print(f'header:{header}')
    print(f'datainfo:{datainfo}')

    search_response = requests.get(url, params=datainfo, headers=header, verify=False, cookies=cookie).json()
    print(search_response)
    requestId = search_response['responseData']['requestId']
    totalNum = search_response['responseData']['totalNum']

    while totalNum == 0:
        datainfo['requestId'] = requestId
        search_response = requests.get(url, params=datainfo, headers=header, verify=False, cookies=cookie).json()
        print(search_response)
        requestId = search_response['responseData']['requestId']
        totalNum = search_response['responseData']['totalNum']
        
    fullPath = search_response['responseData']['data'][0]['fullPath']
    dispPath = search_response['responseData']['data'][0]['dispPath']
    nodeType = search_response['responseData']['data'][0]['nodeType']
    customer = search_response['responseData']['data'][0]['customer']
    uuid = search_response['responseData']['data'][0]['uuid']
    return fullPath, dispPath, nodeType, customer, uuid

@pytest.fixture()
def vmwarepath_from_uuid(get_baseurl, get_version, login_operator, platform_details_from_IP, get_vmwaredatasource, get_Builtin_Client_Id, get_timestamp):
    """获取vmware备份数据源的fullpath,dispath"""
    file = open('/eisoo/CZB-Test/workspace/4-0-Prepare_Job/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    jobVplatformIP, jobVplatformName, jobVplatformId, version = platform_details_from_IP
    builtin_client_Id = get_Builtin_Client_Id
    timestamp = get_timestamp

    url = parse.urljoin(base_url, res['vmware_fullpath_url']).format(builtin_client_Id)
    referer = parse.urljoin(base_url, res['vmware_fullpath_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_operator
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    datainfo = {"fullPath": "%s" %jobVplatformIP,
                "type": 12000,
                "uuid": "",
                "jobType": "eso_backupengine_vmwareengine",
                "options[clientType]": "",
                "options[engineType]": "",
                "index": 0,
                "count": 100,
                "requestId": "",
                "code": "",
                "customer": "{\"mode\": \"host\"}",
                "vplatformId": "%s" %jobVplatformId,
                "partialSign": 0,
                "_": timestamp}
    print(f'url:{url}')
    print(f'header:{header}')
    print(f'datainfo:{datainfo}')

    vmwarepath_response_a = requests.get(url, params=datainfo, headers=header, verify=False, cookies=cookie).json()
    print(vmwarepath_response_a)
    requestId = vmwarepath_response_a['responseData']['requestId']
    datainfo = {"fullPath": "%s" %jobVplatformIP,
                "type": 12000,
                "uuid": "",
                "jobType": "eso_backupengine_vmwareengine",
                "options[clientType]": "",
                "options[engineType]": "",
                "index": 0,
                "count": 100,
                "requestId": "%s" %requestId,
                "code": "",
                "customer": "{\"mode\": \"host\"}",
                "vplatformId": "%s" %jobVplatformId,
                "partialSign": 0,
                "_": timestamp+500}
    print(f'url:{url}')
    print(f'header:{header}')
    print(f'datainfo:{datainfo}')
    sleep(5)
    vmwarepath_response_b = requests.get(url, params=datainfo, headers=header, verify=False, cookies=cookie).json()
    print(vmwarepath_response_b)
    
    nodeType = vmwarepath_response_b['responseData']['data'][0]['nodeType']
    fullPath = vmwarepath_response_b['responseData']['data'][0]['fullPath']
    uuid = vmwarepath_response_b['responseData']['data'][0]['uuid']
    
    while uuid != get_vmwaredatasource:
        timestamp = get_timestamp
        datainfo = {"fullPath": "%s" %fullPath,
                "type": "%s" %nodeType,
                "uuid": "",
                "jobType": "eso_backupengine_vmwareengine",
                "options[clientType]": "",
                "options[engineType]": "",
                "index": 0,
                "count": 100,
                "requestId": "",
                "code": "",
                "customer": "{\"mode\": \"host\"}",
                "vplatformId": "%s" %jobVplatformId,
                "partialSign": 0,
                "_": timestamp}
        vmwarepath_response_a = requests.get(url, params=datainfo, headers=header, verify=False, cookies=cookie).json()
        datainfo['requestId'] = vmwarepath_response_a['responseData']['requestId']
        datainfo['_'] = timestamp+500
        sleep(5)
        print(datainfo)
        vmwarepath_response_b = requests.get(url, params=datainfo, headers=header, verify=False, cookies=cookie).json()
        print(vmwarepath_response_b)
        nodeType = vmwarepath_response_b['responseData']['data'][0]['nodeType']
        fullPath = vmwarepath_response_b['responseData']['data'][0]['fullPath']
        uuid = vmwarepath_response_b['responseData']['data'][0]['uuid']
    else:
        totalNum = vmwarepath_response_b['responseData']['totalNum']
        i = 0
        while i < totalNum:
            if vmwarepath_response_b['responseData']['data'][i]['uuid'] == get_vmwaredatasource:
                fullPath = vmwarepath_response_b['responseData']['data'][i]['fullPath']
                dispPath = vmwarepath_response_b['responseData']['data'][i]['dispPath']
                nodeType = vmwarepath_response_b['responseData']['data'][i]['nodeType']
                customer = vmwarepath_response_b['responseData']['data'][i]['customer']
                uuid = vmwarepath_response_b['responseData']['data'][i]['uuid']
                print(fullPath, dispPath, nodeType, customer, uuid)
                return fullPath, dispPath, nodeType, customer, uuid
            else:
                i += 1
            

@pytest.fixture()
def get_filedispath(get_fullpath):
    """将文件备份任务fullpath拆分为dispath"""
    fullpath = get_fullpath
    #dispath = fullpath.split('/')
    dispath = list(filter(None, fullpath.split('/')))
    print(dispath)
    return dispath

@pytest.fixture()
def get_Builtin_Client_Id(get_baseurl, get_version, login_operator):
    """获取任意一个内置客户端的Id"""
    file = open('/eisoo/CZB-Test/workspace/4-0-Prepare_Job/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    url = parse.urljoin(base_url, res['client_idSet_url'])
    referer = parse.urljoin(base_url, res['client_idSet_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_operator
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    datainfo = {"clientIsBuildIn": "",
                "clientType": 1,
                "count": 15,
                "filterType": 5,
                "index": 0,
                "isClient": "true",
                "ngDialogId": "ngdialog19"}

    print(f'builtin_client_url:{url}')
    print(f'builtin_client_header:{header}')
    print(f'builtin_client_datainfo:{datainfo}')

    builtin_client_response = requests.get(url, params=datainfo, headers=header, verify=False, cookies=cookie).json()
    print(builtin_client_response)
    return builtin_client_response['responseData']['data'][0]['clientId']

@pytest.fixture()
def platform_verify(get_baseurl, get_version, login_operator, get_vmwareip):
    """获取虚拟化平台证书"""
    file = open('/eisoo/CZB-Test/workspace/4-0-Prepare_Job/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0', '7.0.12.0', '7.0.13.0'):
        return False
    url = parse.urljoin(base_url, res['verify_url'])
    referer = parse.urljoin(base_url, res['verify_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_operator
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    host = get_vmwareip
    datainfo = {"host": "%s" %host,
                "port": ""}

    print(f'url:{url}')
    print(f'header:{header}')
    print(f'datainfo:{datainfo}')

    response = requests.get(url, params=datainfo, headers=header, verify=False, cookies=cookie).json()
    print(response)
    return response['responseData']['fingerprint']

@pytest.fixture()
def get_oracle_customer(get_baseurl, get_version, login_operator, login_sadmin, get_oracleclientip, get_oracleDatabaseName, get_timestamp, get_groupId):
    """获取Oracle任务所需的customer"""
    file = open('/eisoo/CZB-Test/workspace/4-0-Prepare_Job/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    timestamp = get_timestamp
    clientId, clientName = common.client_details_from_IP(base_url, version, login_sadmin, get_oracleclientip)

    url = parse.urljoin(base_url, res['oracle_customer_url']).format(clientId)
    referer = parse.urljoin(base_url, res['oracle_customer_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_operator
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    datainfo = {"fullPath": "",
                "jobType": "eso_backupengine_oracleengine",
                "options[clientType]": "",
                "options[engineType]": "",
                "uuid": "",
                "index": 0,
                "count": 1000,
                "requestId": "",
                "type": 1000,
                "code": "",
                "customer": "",
                "svcType": 1,
                "osUserName": "oracle",
                "partialSign": 0,
                "_": timestamp}

    print(f'url:{url}')
    print(f'header:{header}')
    print(f'datainfo:{datainfo}')

    response = requests.get(url, params=datainfo, headers=header, verify=False, cookies=cookie).json()
    print(response)
    requestId = response['responseData']['requestId']
    print(requestId)
    
    datainfo['requestId'] = requestId
    timestamp = get_timestamp
    datainfo['_'] = timestamp
    response = requests.get(url, params=datainfo, headers=header, verify=False, cookies=cookie).json()
    print(response)
    datasource = get_oracleDatabaseName
    totalNum = response['responseData']['totalNum']
    i = 0
    while i < totalNum:
        if response['responseData']['data'][i]['dispPath'] == datasource:
            print(response['responseData']['data'][i]['customer'])
            return response['responseData']['data'][i]['customer']
        else:
            i += 1

@pytest.fixture()
def get_oracle_user(get_baseurl, get_version, login_operator, login_sadmin, get_oracleclientip, get_groupId):
    """获取Oracle任务的osUserName"""
    file = open('/eisoo/CZB-Test/workspace/4-0-Prepare_Job/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    clientId, clientName = common.client_details_from_IP(base_url, version, login_sadmin, get_oracleclientip)

    url = parse.urljoin(base_url, res['oracle_user_url']).format(clientId)
    referer = parse.urljoin(base_url, res['oracle_user_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_operator
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    datainfo = {"isOnClientMgm": "true",
                "jobType": "eso_backupengine_oracleengine",
                "osUserName": ""}

    print(f'url:{url}')
    print(f'header:{header}')
    print(f'datainfo:{datainfo}')

    response = requests.get(url, params=datainfo, headers=header, verify=False, cookies=cookie).json()
    print(response)
    return response['responseData']['data'][0]['user']

@pytest.fixture()
def get_timestamp():
    t = time.time()
    timestamp = int(round(t*1000))
    print(timestamp)
    return timestamp 

