import sys
sys.path.append("/eisoo/CZB-Test/workspace/")
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
        "--VolumeNodeIP", action="store", default="False"
    )
    parser.addoption(
        "--SoftVolumeNodeIP", action="store", default="False"
    )
    parser.addoption(
        "--SnapPoolNodeIP", action="store", default="False"
    )
    parser.addoption(
        "--AMSIPOrDomain", action="store", default="False"
    )
    parser.addoption(
        "--License.dat", action="store", default="False"
    )
    parser.addoption(
        "--Active.dat", action="store", default="False"
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

@pytest.fixture()  #获取创建卷的节点IP
def get_volumenodeIP(pytestconfig):
    VolumeNodeIP = pytestconfig.getoption('--VolumeNodeIP')
    if VolumeNodeIP == '':
        return False
    else:
        return VolumeNodeIP

@pytest.fixture()  #获取创建卷的节点IP
def get_softvolumenodeIP(pytestconfig):
    print(pytestconfig.getoption('--SoftVolumeNodeIP'))
    SoftVolumeNodeIP = pytestconfig.getoption('--SoftVolumeNodeIP')
    if SoftVolumeNodeIP == '':
        return False
    else:
        return SoftVolumeNodeIP

@pytest.fixture()  #获取创建存储池的节点IP
def get_snappoolnodeIP(pytestconfig):
    print(pytestconfig.getoption('--SnapPoolNodeIP'))
    SnapPoolNodeIP = pytestconfig.getoption('--SnapPoolNodeIP')
    if SnapPoolNodeIP == '':
        return False
    else:
        return SnapPoolNodeIP

@pytest.fixture()  #获取待接入的AMS
def get_amsIPorDomain(pytestconfig):
    print(pytestconfig.getoption('--AMSIPOrDomain'))
    AMSIPOrDomain = pytestconfig.getoption('--AMSIPOrDomain')
    if AMSIPOrDomain == '':
        return False
    else:
        return AMSIPOrDomain

@pytest.fixture()
def login_Initialadmin(get_baseurl, get_version):
    """获取未初始化的admin用户的cookie"""
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    url = parse.urljoin(base_url, res['login_url'])
    referer = parse.urljoin(base_url, res['login_referer'])
    header = {'referer': '%s' %(referer)}
    datainfo = {"userName": "admin",
                "userPass": "inHFKrXPDogXBThOMNe5xFAD04VtVNc+xBlK+gx5KFQll6HnexSDQx3j+Wu20H+4Hx7cCw56JE4ucAa2fy2l0ZZnSgSEPBa+yMl5200q8jGE4hXQTe0zVw1FNV5mN5jSkYrsFQCKsrSEhRhZajJCG6gOXUhUt8Ex5XqR7VFRIrM=",  # P@ssword123
                "validPwdExpire": "true",
                "isEnc": "true"}
    admin_login_response = requests.post(url, headers=header, json=datainfo, verify=False)
    if admin_login_response.json()['status'] != "success":
        # 若admin已初始化完成，不需要再进行初始化，则返回False
        return False
    elif version in ('7.0.8.0','7.0.9.1','7.0.10.0','7.0.11.0'):
        cookie = admin_login_response.cookies
        userId = admin_login_response.cookies['userId']
        return cookie, userId
    else:
        cookie = admin_login_response.cookies
        userId = admin_login_response.cookies['userId']
        csrftoken = admin_login_response.cookies['csrftoken']
        return cookie, userId, csrftoken

@pytest.fixture()
def login_Initialsadmin(get_baseurl, get_version):
    """获取未初始化的sadmin用户的cookie"""
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    print(version)

    url = parse.urljoin(base_url, res['login_url'])
    referer = parse.urljoin(base_url, res['login_referer'])
    header = {'referer': '%s' %(referer)}
    datainfo = {"userName": "sadmin",
                "userPass": "inHFKrXPDogXBThOMNe5xFAD04VtVNc+xBlK+gx5KFQll6HnexSDQx3j+Wu20H+4Hx7cCw56JE4ucAa2fy2l0ZZnSgSEPBa+yMl5200q8jGE4hXQTe0zVw1FNV5mN5jSkYrsFQCKsrSEhRhZajJCG6gOXUhUt8Ex5XqR7VFRIrM=",  # P@ssword123
                "validPwdExpire": "true",
                "isEnc": "true"}
    sadmin_login_response = requests.post(url, headers=header, json=datainfo, verify=False)
    print(sadmin_login_response.json())
    if sadmin_login_response.json()['status'] != "success":
        # 若sadmin已初始化完成，不需要在进行初始化则返回False
        return False
    elif version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie = sadmin_login_response.cookies
        userId = sadmin_login_response.cookies['userId']
        return cookie, userId
    else:
        cookie = sadmin_login_response.cookies
        userId = sadmin_login_response.cookies['userId']
        csrftoken = sadmin_login_response.cookies['csrftoken']
        return cookie, userId, csrftoken

@pytest.fixture()
def login_Initialoperator(get_baseurl, get_version):
    """获取未初始化的admin用户的cookie"""
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    print(version)

    url = parse.urljoin(base_url, res['login_url'])
    referer = parse.urljoin(base_url, res['login_referer'])
    header = {'referer': '%s' %(referer)}
    datainfo = {"userName": "test",
                "userPass": "inHFKrXPDogXBThOMNe5xFAD04VtVNc+xBlK+gx5KFQll6HnexSDQx3j+Wu20H+4Hx7cCw56JE4ucAa2fy2l0ZZnSgSEPBa+yMl5200q8jGE4hXQTe0zVw1FNV5mN5jSkYrsFQCKsrSEhRhZajJCG6gOXUhUt8Ex5XqR7VFRIrM=",  # P@ssword123
                "validPwdExpire": "true",
                "isEnc": "true"}
    operator_login_response = requests.post(url, headers=header, json=datainfo, verify=False)
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie = operator_login_response.cookies
        userId = operator_login_response.cookies['userId']
        return cookie, userId
    else:
        cookie = operator_login_response.cookies
        userId = operator_login_response.cookies['userId']
        csrftoken = operator_login_response.cookies['csrftoken']
        return cookie, userId, csrftoken

@pytest.fixture()
def login_admin(get_baseurl, get_version):
    """获取admin用户的cookie"""
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
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
def login_sadmin(get_baseurl, get_version):
    """获取sadmin用户的cookie"""
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
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
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie = sadmin_login_response.cookies
        userId = sadmin_login_response.cookies['userId']
        return cookie, userId
    else:
        cookie = sadmin_login_response.cookies
        userId = sadmin_login_response.cookies['userId']
        csrftoken = sadmin_login_response.cookies['csrftoken']
        return cookie, userId, csrftoken

@pytest.fixture()
def nodes_idSet(get_baseurl, get_version, login_admin):
    """获取控制台所有节点的id列表"""
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    url = parse.urljoin(base_url, res['nodes_idSet_url'])
    referer = parse.urljoin(base_url, res['nodes_idSet_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_admin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_admin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}

    nodes_idSet_response = requests.get(url, headers=header, verify=False, cookies=cookie).json()
    totalNum = nodes_idSet_response['responseData']['totalNum']
    i = 0
    nodes_ip = []
    nodes_id = []
    while i < totalNum:
        nodes_ip.append(nodes_idSet_response['responseData']['data'][i]['nodeIp'])
        nodes_id.append(nodes_idSet_response['responseData']['data'][i]['id'])
        i += 1
    return nodes_ip, nodes_id

@pytest.fixture()
def node_idSet(get_baseurl, get_version, get_volumenodeIP, login_admin):
    """获取控制台指定节点的id"""
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    volumenodeIP = get_volumenodeIP

    url = parse.urljoin(base_url, res['nodes_idSet_url'])
    referer = parse.urljoin(base_url, res['nodes_idSet_referer'])
    if get_volumenodeIP == False:
        pytest.skip(msg='This test is only for Apollo Console')
    elif version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_admin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_admin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}

    node_idSet_response = requests.get(url, headers=header, verify=False, cookies=cookie).json()
    totalNum = node_idSet_response['responseData']['totalNum']

    i = 0
    while i < totalNum:
        if node_idSet_response['responseData']['data'][i]['nodeIp'] == volumenodeIP:
            return node_idSet_response['responseData']['data'][i]['id']
        else:
            i += 1
            continue

@pytest.fixture()
def node_idSet_Soft(get_baseurl, get_version, get_softvolumenodeIP, login_admin):
    """获取控制台指定节点的id"""
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    volumenodeIP = get_softvolumenodeIP

    url = parse.urljoin(base_url, res['nodes_idSet_url'])
    referer = parse.urljoin(base_url, res['nodes_idSet_referer'])
    if get_softvolumenodeIP == False:
        pytest.skip(msg='This test is only for CentOS Console')
    elif version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_admin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_admin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}

    node_idSet_response = requests.get(url, headers=header, verify=False, cookies=cookie).json()
    totalNum = node_idSet_response['responseData']['totalNum']

    i = 0
    while i < totalNum:
        if node_idSet_response['responseData']['data'][i]['nodeIp'] == volumenodeIP:
            return node_idSet_response['responseData']['data'][i]['id']
        else:
            i += 1
            continue

@pytest.fixture()
def node_idSet_pool(get_baseurl, get_version, get_snappoolnodeIP, login_admin):
    """获取控制台指定节点的id"""
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    snappoolnodeIP = get_snappoolnodeIP

    url = parse.urljoin(base_url, res['nodes_idSet_url'])
    referer = parse.urljoin(base_url, res['nodes_idSet_referer'])
    if get_snappoolnodeIP == False:
        pytest.skip(msg='This test is only for Apollo Console')
    elif version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_admin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_admin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}

    node_idSet_response = requests.get(url, headers=header, verify=False, cookies=cookie).json()
    totalNum = node_idSet_response['responseData']['totalNum']

    i = 0
    while i < totalNum:
        if node_idSet_response['responseData']['data'][i]['nodeIp'] == snappoolnodeIP:
            print(node_idSet_response['responseData']['data'][i]['id'])
            return node_idSet_response['responseData']['data'][i]['id']
        else:
            i += 1
            continue

@pytest.fixture()
def raid_YesorNo(get_baseurl, login_admin, node_idSet, get_version):
    """判断节点上是否已经存在raid"""
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    datainfo = {"count": 15,
                "index": 0,
                "raidModel": "-"}
    datainfo['nodeId'] = node_idSet
    url = parse.urljoin(base_url, res['raidcatch_url'])
    referer = parse.urljoin(base_url, res['raidcatch_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_admin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_admin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}

    raid_YesorNo_response = requests.get(url, headers=header, params=datainfo, verify=False, cookies=cookie).json()
    totalNum = raid_YesorNo_response['responseData']['totalNum']
    print(raid_YesorNo_response)
    if totalNum >= 1:
        return False
    else:
        return True

@pytest.fixture()
def raid_catch(get_baseurl, get_version, login_admin, node_idSet, get_volumenodeIP):
    """获取raid信息"""
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    
    if get_volumenodeIP == False:
        pytest.skip(msg='This test is only for Apollo Console')

    datainfo = {}
    datainfo["nodeId"] = "%s" %(node_idSet)
    datainfo["nodeIp"] = get_volumenodeIP
    url = parse.urljoin(base_url, res['raidcatch_url'])
    referer = parse.urljoin(base_url, res['raidcatch_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_admin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_admin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}

    raid_catch_response = requests.get(url, headers=header, params=datainfo, verify=False, cookies=cookie).json()
    print(raid_catch_response)
    raidTotal = raid_catch_response['responseData']['data'][0]['raidTotal']
    raidUsable = raid_catch_response['responseData']['data'][0]['raidUsable']
    raidName = raid_catch_response['responseData']['data'][0]['raidName']
    raidType = raid_catch_response['responseData']['data'][0]['raidType']
    print(raidTotal, raidName, raidType)
    return raidTotal, raidUsable, raidName, raidType

@pytest.fixture()
def disk_catch(login_admin, get_baseurl, node_idSet, get_volumenodeIP, get_version, raid_YesorNo):
    """获取新建raid可用的磁盘"""
    if raid_YesorNo:
        file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
        # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
        res = yaml.load(file, Loader=yaml.FullLoader)
        base_url = get_baseurl

        if get_volumenodeIP == False:
            pytest.skip(msg='This test is only for Apollo Console')

        version = get_version
        url = parse.urljoin(base_url, res['disk_url'])
        referer = parse.urljoin(base_url, res['disk_referer'])
        if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
            cookie, userId = login_admin
            header = {"referer": "%s" % (referer)}
        else:
            cookie, userId, csrftoken = login_admin
            header = {"referer": "%s" % (referer),
                      "x-csrftoken": "%s" % (csrftoken)}

        datainfo = {"count": 15,
                    "idle": 1,
                    "index": 0,
                    "raidModel": "-"
                    }
        datainfo["nodeId"] = node_idSet
        datainfo["nodeIP"] = get_volumenodeIP

        disk_catch_response = requests.get(url, headers=header, params=datainfo, cookies=cookie, verify=False).json()
        print(disk_catch_response)

        if disk_catch_response['responseData']['totalNum'] >= 1:
            diskId01 = disk_catch_response['responseData']['data'][0]['devId']
            return diskId01
        return False

@pytest.fixture()
def path_catch(login_admin, get_baseurl, node_idSet_Soft, get_version):
    """获取软件版控制台可用的卷挂载路径"""
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl

    version = get_version
    url = parse.urljoin(base_url, res['path_url'])
    referer = parse.urljoin(base_url, res['path_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_admin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_admin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}

    datainfo = {"index": 0,
                "count": 50,
                "requestId": "",
                "type": 1,
                "_": 1615343848622}
    datainfo["nodeId"] = node_idSet_Soft

    path_catch_response = requests.get(url, headers=header, params=datainfo, cookies=cookie, verify=False).json()
    print(path_catch_response)
    usablePath = path_catch_response['responseData']['data'][0]['path']
    freeSize = path_catch_response['responseData']['data'][0]['freeSize']

    return usablePath, freeSize

@pytest.fixture()
def mdisks_catch(login_admin, get_baseurl, get_snappoolnodeIP, get_version):
    """获取创建存储池可用的mdisks"""
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl

    version = get_version
    url = parse.urljoin(base_url, res['mdisks_url'])
    referer = parse.urljoin(base_url, res['mdisks_referer'])
    print(get_snappoolnodeIP)
    
    if get_snappoolnodeIP == False:
        pytest.skip(msg='Don not run')
    elif version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_admin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_admin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}

    datainfo = {"filter": "true",
                "poolId": "false"}
    datainfo["nodeIp"] = get_snappoolnodeIP

    mdisks_catch_response = requests.get(url, headers=header, params=datainfo, cookies=cookie, verify=False).json()
    print(mdisks_catch_response)
    diskId = mdisks_catch_response['responseData'][0]['diskId']

    return diskId

@pytest.fixture()
def clients_idSet(get_baseurl, get_version, login_sadmin):
    """获取控制台所有客户端的id列表"""
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    url = parse.urljoin(base_url, res['client_idSet_url'])
    referer = parse.urljoin(base_url, res['client_idSet_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_sadmin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_sadmin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    datainfo = {"clientIsBuildin": "false",
                "count": 15,
                "filter": "",
                "includeSubUser": "true",
                "index": 0}

    clients_idSet_response = requests.get(url, params=datainfo, headers=header, verify=False, cookies=cookie).json()
    print(clients_idSet_response)
    totalNum = clients_idSet_response['responseData']['totalNum']
    i = 0
    clientsId = []
    while i < totalNum:
        clientsId.append(clients_idSet_response['responseData']['data'][i]['clientId'])
        i += 1
    return clientsId

@pytest.fixture()
def login_operator(get_baseurl):
    """获取操作员用户的cookie"""
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl

    url = parse.urljoin(base_url, res['login_url'])
    referer = parse.urljoin(base_url, res['login_referer'])
    header = {'referer': '%s' %(referer)}
    datainfo = {"userName": "test",
                "userPass": "DdiclnSMWi8n20cXSCiQbj0UOZpMUl8zxcf01fBv1LXzS4VVGanOkbhqhpgXzVys7yVLjpzUr3S/OqVoaUUP/MzVIOUtOB9J1dIa//zW6S0pumm/Ybnqmd+erN7Kj2MUfSnR/adhmu6DPCFmkYZM1lA6rIWKx5oiTX5imHFNJ3M=",  # eisoo.com123
                "validPwdExpire": "true",
                "isEnc": "true"}
    test_login_response = requests.post(url, headers=header, json=datainfo, verify=False)
    cookie = test_login_response.cookies
    return cookie

@pytest.fixture()
def fp_nodeIps(get_baseurl, get_version, login_operator):
    """获取控制台所有客户端的id列表"""
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    url = parse.urljoin(base_url, res['fp_nodeips_url'])
    referer = parse.urljoin(base_url, res['fp_nodeips_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie = login_operator
        csrftoken = cookie['csrftoken']
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
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    url = parse.urljoin(base_url, res['fp_Guid_url'])
    referer = parse.urljoin(base_url, res['fp_Guid_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie = login_operator
        csrftoken = cookie['csrftoken']
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
    """获取客户端资源中默认组的"""
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    url = parse.urljoin(base_url, res['groupId_url'])
    referer = parse.urljoin(base_url, res['groupId_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie = login_operator
        csrftoken = cookie['csrftoken']
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
def client_details_from_IP(get_baseurl, get_version, login_operator, get_clientip, get_groupId):
    """通过客户端IP获取客户端的其他信息"""
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    url = parse.urljoin(base_url, res['client_idSet_url'])
    referer = parse.urljoin(base_url, res['client_idSet_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie = login_operator
        csrftoken = cookie['csrftoken']
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    datainfo = {"count": 15,
                "excludeTypes": 7,
                "filter": "",
                "index": 0}
    datainfo['groupId'] = get_groupId

    client_details_from_IP_response = requests.get(url, params=datainfo, headers=header, verify=False, cookies=cookie).json()
    print(client_details_from_IP_response)
    totalNum = client_details_from_IP_response['responseData']['totalNum']
    i = 0
    while i < totalNum:
        if client_details_from_IP_response['responseData']['data'][i]['clientIp'] == get_clientip:
            clientId = client_details_from_IP_response['responseData']['data'][i]['clientId']
            clientName = client_details_from_IP_response['responseData']['data'][i]['clientName']
            return clientId, clientName
        i += 1

@pytest.fixture()
def file_flib_idSet(get_baseurl, get_version, login_operator):
    """获取文件类型的指纹库ID"""
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    url = parse.urljoin(base_url, res['flib_idSet_url'])
    referer = parse.urljoin(base_url, res['flib_idSet_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie = login_operator
        csrftoken = cookie['csrftoken']
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    datainfo = {"count": 8,
                "index": 0,
                "jobType": "eso_backupengine_fileengine"}
    print(url)
    print(header)
    print(datainfo)

    file_flib_idSet_response = requests.get(url, params=datainfo, headers=header, verify=False, cookies=cookie).json()
    print(file_flib_idSet_response)
    file_flib_idSet = file_flib_idSet_response['responseData']['data'][0]['fpGuid']
    return file_flib_idSet

@pytest.fixture()
def jobId_from_jobName(get_baseurl, get_version, login_operator):
    """获取指定任务的id"""
    file = open('/eisoo/CZB-Test/workspace/2-0-Configure_Console/TestData/config.yaml')
    # file = open('D:\\2-1-Configure_Console\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    url = parse.urljoin(base_url, res['jobId_url'])
    referer = parse.urljoin(base_url, res['jobId_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie = login_operator
        csrftoken = cookie['csrftoken']
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    datainfo = {"count": 15,
                "index": 0,
                "status": ""}
    print(url)
    print(header)
    print(datainfo)

    jobId_from_jobName_response = requests.get(url, params=datainfo, headers=header, verify=False, cookies=cookie).json()
    print(jobId_from_jobName_response)
    totalNum = jobId_from_jobName_response['responseData']['totalNum']
    i = 0
    while i < totalNum:
        if jobId_from_jobName_response['responseData']['data'][i]['jobName'] == 'file01':
            jobId = jobId_from_jobName_response['responseData']['data'][i]['jobId']
            return jobId
        i += 1





