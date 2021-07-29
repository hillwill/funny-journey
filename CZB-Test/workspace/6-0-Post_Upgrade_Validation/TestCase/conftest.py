import sys
sys.path.append("/eisoo/CZB-Test/workspace/")
import pytest
import yaml
from urllib import parse
import requests
import time
import paramiko
from common import common
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
        "--file_ClientIP", action="store", default="False"
    )
    parser.addoption(
        "--file_ClientPwd", action="store", default=""
    )
    parser.addoption(
        "--file_DataSource", action="store", default=""
    )
    parser.addoption(
        "--oracle_ClientIP", action="store", default="False"
    )
    parser.addoption(
        "--oracle_ClientPwd", action="store", default=""
    )
    parser.addoption(
        "--oracle_DatabaseName", action="store", default=""
    )
    parser.addoption(
        "--vmware_IP", action="store", default="False"
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

@pytest.fixture()  #获取文件回复任务目标客户端IP
def get_clientip(pytestconfig):
    print(pytestconfig.getoption('--file_ClientIP'))
    file_ClientIP = pytestconfig.getoption('--file_ClientIP')
    if file_ClientIP == '':
        return False
    else:
        return file_ClientIP

@pytest.fixture()  #获取文件备份任务客户端密码
def get_clientpwd(pytestconfig):
    print(pytestconfig.getoption('--file_ClientPwd'))
    file_ClientPwd = pytestconfig.getoption('--file_ClientPwd')
    return file_ClientPwd

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

@pytest.fixture()  #获取oracle任务客户端密码
def get_oracleclientpwd(pytestconfig):
    print(pytestconfig.getoption('--oracle_ClientPwd'))
    oracle_ClientPwd = pytestconfig.getoption('--oracle_ClientPwd')
    return oracle_ClientPwd

@pytest.fixture()   #获取oracle的数据库名
def get_oracleDatabaseName(pytestconfig):
    oracle_DatabaseName = pytestconfig.getoption('--oracle_DatabaseName')
    return oracle_DatabaseName

@pytest.fixture()  #获取VMware任务的平台IP
def get_vmwareip(pytestconfig):
    print(pytestconfig.getoption('--vmware_IP'))
    vmware_IP = pytestconfig.getoption('--vmware_IP')
    if vmware_IP == '':
        return False
    else:
        return vmware_IP

@pytest.fixture()
def login_operator(get_baseurl, get_version):
    """获取操作员用户的cookie"""
    file = open('/eisoo/CZB-Test/workspace/6-0-Post_Upgrade_Validation/TestData/config.yaml')
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
def login_sadmin(get_baseurl, get_version):
    """获取sadmin用户的cookie"""
    file = open('/eisoo/CZB-Test/workspace/6-0-Post_Upgrade_Validation/TestData/config.yaml')
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
def platform_details_from_IP(get_baseurl, get_version, login_operator, get_vmwareip):
    """获取VMware平台的具体信息"""
    file = open('/eisoo/CZB-Test/workspace/6-0-Post_Upgrade_Validation/TestData/config.yaml')
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
    print(url)
    print(header)
    print(datainfo)

    platform_details_response = requests.get(url, params=datainfo, headers=header, verify=False, cookies=cookie).json()
    print(platform_details_response)
    totalNum = platform_details_response['responseData']['totalNum']
    i = 0
    while i < totalNum:
        if platform_details_response['responseData']['data'][i]['ip'] == get_vmwareip:
            jobVplatformIP = platform_details_response['responseData']['data'][i]['ip']
            jobVplatformName = platform_details_response['responseData']['data'][i]['name']
            jobVplatformId = platform_details_response['responseData']['data'][i]['id']
            version = platform_details_response['responseData']['data'][i]['version']
            return jobVplatformIP, jobVplatformName, jobVplatformId, version
        i += 1

@pytest.fixture()
def cluster_idSet(login_operator, get_baseurl, get_version):
    """获取集群id及其他信息"""
    file = open("/eisoo/CZB-Test/workspace/6-0-Post_Upgrade_Validation/TestData/config.yaml")
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    
    url = parse.urljoin(base_url, res['cluster_idSet_url'])
    referer = parse.urljoin(base_url, res['cluster_idSet_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_operator
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    datainfo = {"cerify": 1,
                "count": 0,
                "filter": "",
                "includeLocal": "true",
                "index": 0,
                "type": 1}
    print(url)
    print(header)
    print(datainfo)
    
    cluster_idSet_response = requests.get(url, params=datainfo, headers=header, verify=False, cookies=cookie).json()
    print(cluster_idSet_response)
    clusterId = cluster_idSet_response['responseData']['data'][0]['clusterId']
    vip = cluster_idSet_response['responseData']['data'][0]['vip']
    return clusterId, vip


@pytest.fixture()
def get_groupId(get_baseurl, get_version, login_operator):
    """获取客户端资源中默认组的"""
    file = open("/eisoo/CZB-Test/workspace/6-0-Post_Upgrade_Validation/TestData/config.yaml")
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
def diff_filemd5(get_clientip, get_fullpath, get_clientpwd):
    """恢复后对比文件备份任务数据源的md5值"""
    ip = get_clientip
    port = 22
    password = get_clientpwd
    fullpath = get_fullpath
    print(ip)
    print(password)
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
        stdin, stdout, stderr = ssh.exec_command('find %s -type f -print0 | xargs -0 md5sum > /var/log/md5_2.log' %(fullpath))
        print(stdout.read().decode('utf-8'))
        print('md5值计算完成:%s'%ip)
    except Exception as e:
        print('md5值计算错误:%s' %ip, e)

    try:
        stdin, stdout, stderr = ssh.exec_command('diff /var/log/md5.log /var/log/md5_2.log')
        out = stdout.read().decode('utf-8')
        print(out)
        print('md5值对比完成:%s'%ip)
    except Exception as e:
        print('md5值对比错误:%s' %ip, e)

    return out

@pytest.fixture()
def get_oracle_user(get_baseurl, get_version, login_operator, login_sadmin, get_oracleclientip, get_groupId):
    """获取Oracle任务的osUserName"""
    file = open("/eisoo/CZB-Test/workspace/6-0-Post_Upgrade_Validation/TestData/config.yaml")
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
def platform_details_from_IP(get_baseurl, get_version, login_operator, get_vmwareip):
    """获取VMware平台的具体信息"""
    file = open("/eisoo/CZB-Test/workspace/6-0-Post_Upgrade_Validation/TestData/config.yaml")
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
def get_Builtin_Client_Id(get_baseurl, get_version, login_operator):
    """获取任意一个内置客户端的Id"""
    file = open("/eisoo/CZB-Test/workspace/6-0-Post_Upgrade_Validation/TestData/config.yaml")
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
