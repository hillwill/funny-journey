import sys
sys.path.append("D:\\MyProject\\Api-test")
from urllib import parse
import pytest
import requests
import yaml
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import re

@pytest.fixture()
def login_newadmin():
    """
    获取管理员admin账户的cookies
    """
    file = open('D:\MyProject\Api-test\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['login_url'])
    header = res['login_headers']
    datainfo={"userName": "admin",
              "userPass": "Lx+vJdrqkEcRiWTUNqfWFGQD+xvKH4wHjn22sm4iuwQvFyM2JsNXKGWqN05lkmPQaCObxiJlxnAM3SDNzT1PmMQs9pn/LTQPIAhdH9kYC1Pc25dvyH1qp9jJDymICD+gf4UIaY5WZUGicTpqOlT1dS/eI8gIabYFKH7x4ol2k3Q=",
              "validPwdExpire": "true",
              "isEnc": "true"}
    response=requests.post(url, headers=header, json=datainfo, verify=False)
    print(f'cookie:{response.cookies}')
    return response.cookies

@pytest.fixture()
def login_newsadmin():
    """
    获取管理员sadmin账户的cookies
    """
    file = open('D:\MyProject\Api-test\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['login_url'])
    header = res['login_headers']
    datainfo={"userName":"sadmin",
              "userPass":"Lx+vJdrqkEcRiWTUNqfWFGQD+xvKH4wHjn22sm4iuwQvFyM2JsNXKGWqN05lkmPQaCObxiJlxnAM3SDNzT1PmMQs9pn/LTQPIAhdH9kYC1Pc25dvyH1qp9jJDymICD+gf4UIaY5WZUGicTpqOlT1dS/eI8gIabYFKH7x4ol2k3Q=",
              "validPwdExpire":"true",
              "isEnc":"true"}
    response=requests.post(url,headers=header,json=datainfo,verify=False)
    return response.cookies

@pytest.fixture()
def login_newoperator():
    """
    获取操作员账户的cookies
    """
    file = open('D:\MyProject\Api-test\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['login_url'])
    header = res['login_headers']
    datainfo={"userName":"wxt",
              "userPass":"Lx+vJdrqkEcRiWTUNqfWFGQD+xvKH4wHjn22sm4iuwQvFyM2JsNXKGWqN05lkmPQaCObxiJlxnAM3SDNzT1PmMQs9pn/LTQPIAhdH9kYC1Pc25dvyH1qp9jJDymICD+gf4UIaY5WZUGicTpqOlT1dS/eI8gIabYFKH7x4ol2k3Q=",
              "validPwdExpire":"true",
              "isEnc":"true"}
    response=requests.post(url,headers=header,json=datainfo,verify=False)
    return response.cookies

@pytest.fixture()
def login_oldadmin():
    """
    获取管理员admin账户的cookies
    """
    file = open('D:\MyProject\Api-test\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['login_url'])
    header = res['login_headers']
    datainfo={"userName":"admin",
              "userPass":"kjDewFgtqcD32e1WFeyPg6CzCCIFolDMUdtfaZmV2tXajmZAqofy4bLlOKO7N/iYSTFcB0D8Bodo53u0Zwrm5zv+szip6+vu0FBWXuZDaBRXuevfw2VpSjz1yEsCuMoog+XOqg/ZG2m4N6708XOpN2yHMwPvJKSFrw+Hko2dpSw=",
              "validPwdExpire":"true",
              "isEnc":"true"}
    response=requests.post(url,headers=header,json=datainfo,verify=False)
    return response.cookies

@pytest.fixture()
def login_oldsadmin():
    """
    获取管理员sadmin账户的cookies
    """
    file = open('D:\MyProject\Api-test\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['login_url'])
    header = res['login_headers']
    datainfo={"userName":"sadmin",
              "userPass":"LDm5VpovKEISErwLXkd4AheRJ/bQ4j87gqo/QjrOw7Exc0cZLN/+ii1lVwh1rX0zchhlGt85W/s+HF6+uZ5II6vZ8Q3wdaCcYTxXY/xwgiRZnLK4jGf4tyr5M5BTTnv0JYbCE+L4VZzynlxpmh8eloQYKX9/av3T0cp40xpsBdM=",
              "validPwdExpire":"true",
              "isEnc":"true"}
    response=requests.post(url,headers=header,json=datainfo,verify=False)
    return response.cookies

@pytest.fixture()
def login_oldoperator():
    """
    获取操作员账户的cookies
    """
    file = open('D:\MyProject\Api-test\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['login_url'])
    header = res['login_headers']
    datainfo={"userName":"wxt",
              "userPass":"LDm5VpovKEISErwLXkd4AheRJ/bQ4j87gqo/QjrOw7Exc0cZLN/+ii1lVwh1rX0zchhlGt85W/s+HF6+uZ5II6vZ8Q3wdaCcYTxXY/xwgiRZnLK4jGf4tyr5M5BTTnv0JYbCE+L4VZzynlxpmh8eloQYKX9/av3T0cp40xpsBdM=",
              "validPwdExpire":"true",
              "isEnc":"true"}
    response=requests.post(url,headers=header,json=datainfo,verify=False)
    return response.cookies

@pytest.fixture()
def admin_idSet(login_newadmin):
    """获取admin用户的id"""
    file = open('D:\MyProject\Api-test\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['profile_url'])
    # print(f'url:{url}')
    header = res['profile_headers']
    # print(f'header:{header}')
    cookie = login_newadmin
    # print(f'cookie:{cookie}')
    response = requests.get(url, headers=header, verify=False, cookies=cookie).json()
    return response['responseData']['userInfo']['userUUID']

@pytest.fixture()
def sadmin_idSet(login_newsadmin):
    """获取sadmin用户的id"""
    file = open('D:\MyProject\Api-test\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['profile_url'])
    # print(f'url:{url}')
    header = res['profile_headers']
    # print(f'header:{header}')
    cookie = login_newsadmin
    # print(f'cookie:{cookie}')
    response = requests.get(url, headers=header, verify=False, cookies=cookie).json()
    return response['responseData']['userInfo']['userUUID']

@pytest.fixture()
def operator_idSet(login_newoperator):
    """获取sadmin用户的id"""
    file = open('D:\MyProject\Api-test\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['profile_url'])
    # print(f'url:{url}')
    header = res['profile_headers']
    # print(f'header:{header}')
    cookie = login_newoperator
    # print(f'cookie:{cookie}')
    response = requests.get(url, headers=header, verify=False, cookies=cookie).json()
    # print(response['responseData']['userInfo']['userUUID'])
    return response['responseData']['userInfo']['userUUID']

@pytest.fixture()
def oldoperator_idSet(login_oldoperator):
    """获取sadmin用户的id"""
    file = open('D:\MyProject\Api-test\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['profile_url'])
    # print(f'url:{url}')
    header = res['profile_headers']
    # print(f'header:{header}')
    cookie = login_oldoperator
    # print(f'cookie:{cookie}')
    response = requests.get(url, headers=header, verify=False, cookies=cookie).json()
    # print(response['responseData']['userInfo']['userUUID'])
    return response['responseData']['userInfo']['userUUID']

@pytest.fixture()
def nodes_idSet(login_oldadmin):
    """获取节点node的id"""
    file = open('D:\MyProject\Api-test\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['nodes_url'])
    header = res['nodes_headers']
    cookie = login_oldadmin
    response = requests.get(url, headers=header, verify=False, cookies=cookie).json()
    return response['responseData']['data'][0]['id']

@pytest.fixture()
def auth_idSet(login_oldadmin):
    """获取授权码的id"""
    file = open('D:\MyProject\Api-test\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['authId_url'])
    header = res['authId_headers']
    datainfo = {"count": 15,
                "index": 0}
    cookie = login_oldadmin
    response = requests.get(url, headers=header, params=datainfo, verify=False, cookies=cookie).json()
    return response['responseData']['data'][0]['id']

@pytest.fixture()
def client_idSet(login_oldadmin):
    """获取客户端的id"""
    file = open('D:\MyProject\Api-test\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['clientId_url'])
    # print(f'url:{url}')
    header = res['clientId_headers']
    # print(f'header:{header}')
    cookie = login_oldadmin
    # print(f'cookie:{cookie}')
    datainfo = {"clientIsBuildin": "false",
                "count": 15,
                "filter": " ",
                "includeSubUser": "true",
                "index": 0}
    response = requests.get(url, headers=header, params=datainfo, verify=False, cookies=cookie).json()
    # print(response['responseData']['data'][0]['clientId'])
    return response['responseData']['data'][0]['clientId']

@pytest.fixture()
def fp_idSet(login_oldadmin):
    """获取指纹池的id"""
    file = open('D:\MyProject\Api-test\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['fpId_url'])
    # print(f'url:{url}')
    header = res['fpId_headers']
    # print(f'header:{header}')
    cookie = login_oldadmin
    # print(f'cookie:{cookie}')
    datainfo = {"count": 15,
                "index": 0}
    # print(datainfo)
    response = requests.get(url, headers=header, params=datainfo, verify=False, cookies=cookie).json()
    # print(response['responseData']['data'][0]['fpId'])
    return response['responseData']['data'][0]['fpId']

@pytest.fixture()
def fp_info(login_oldadmin):
    """获取所有指纹池名"""
    file = open('D:\MyProject\Api-test\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['fpId_url'])
    # print(f'url:{url}')
    header = res['fpId_headers']
    # print(f'header:{header}')
    cookie = login_oldadmin
    # print(f'cookie:{cookie}')
    datainfo = {"count": 15,
                "index": 0}
    # print(datainfo)
    response = requests.get(url, headers=header, params=datainfo, verify=False, cookies=cookie).json()
    # print(response['responseData']['data'][0]['fpName'])
    return response['responseData']['data'][0]['fpName']

@pytest.fixture()
def job_idSet(login_oldoperator):
    """获取任务的id"""
    file = open('D:\MyProject\Api-test\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['jobid_url'])
    header = res['jobid_headers']
    cookie = login_oldoperator
    datainfo = {"count": 15,
                "index": 0,
                "status": ""
                }
    response = requests.get(url=url, headers=header, params=datainfo, verify=False, cookies=cookie).json()
    return response['responseData']['data'][0]['jobId']

@pytest.fixture()
def cluster_idSet(login_oldoperator):
    """获取集群的id"""
    file = open('D:\MyProject\Api-test\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['clusterid_url'])
    header = res['clusterid_headers']
    cookie = login_oldoperator
    datainfo = {"count": 0,
                "index": 0,
                "filter": "",
                "cerify": 1,
                "includeLocal": "true",
                "type": 1}
    response = requests.get(url=url, headers=header, params=datainfo, verify=False, cookies=cookie).json()
    return response['responseData']['data'][0]['clusterId']

@pytest.fixture()
def gns_idSet(login_oldoperator):
    """获取任务的gns"""
    file = open('D:\MyProject\Api-test\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['gns_url'])
    header = res['gns_headers']
    cookie = login_oldoperator
    datainfo = {"count": 15,
                "index": 0}
    response = requests.get(url=url, headers=header, params=datainfo, verify=False, cookies=cookie).json()
    return response['responseData']['data'][0]['gnsPath']

@pytest.fixture()
def timepoint01_idSet(login_oldoperator, gns_idSet, cluster_idSet):
    """获取最新时间点"""
    file = open('D:\MyProject\Api-test\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['timepoint_url'])
    header = res['timepoint_headers']
    cookie = login_oldoperator
    datainfo = {"clusterId": cluster_idSet,
                "clusterVip": "10.2.12.76",
                "endTime": 1493596800000000,
                "gnsPath": gns_idSet,
                "count": 15,
                "jobStorageId": 1,
                "requestId": "",
                "startTime": 1491004800000000,
                "index": 0}
    # print(f'datainfo:{datainfo}')
    response = requests.get(url=url, headers=header, params=datainfo, verify=False, cookies=cookie).json()
    # print(f'response:{response}')
    return response['responseData']['data'][0]['gnsPath']

@pytest.fixture()
def timepointfull_idSet(login_oldoperator, gns_idSet, cluster_idSet):
    """获取最近一个完备时间点时间点"""
    file = open('D:\MyProject\Api-test\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['timepoint_url'])
    header = res['timepoint_headers']
    cookie = login_oldoperator
    datainfo = {"clusterId": cluster_idSet,
                "clusterVip": "10.2.12.76",
                "endTime": 1493596800000000,
                "gnsPath": gns_idSet,
                "count": 15,
                "jobStorageId": 1,
                "requestId": "",
                "startTime": 1491004800000000,
                "index": 0}
    response = requests.get(url=url, headers=header, params=datainfo, verify=False, cookies=cookie).json()
    i = 0
    for i in range(0,10):
        if response['responseData']['data'][i]['backupType'] == 1:
            return response['responseData']['data'][i]['gnsPath']
        else:
            i += 1

@pytest.fixture()
def timestamptopoint(timepoint02_idSet, timepoint03_idSet):
    """将时间戳转换成备份时间点"""
    timestamp = timepoint02_idSet
    print(f'timestamp:{timestamp}')
    timestamp_ten = timestamp / 1000000
    timearray = time.localtime(timestamp_ten)
    lasttime = time.strftime("%Y-%m-%d %H:%M:%S", timearray)

    backupType = timepoint03_idSet
    timepoint = lasttime + "(" + backupType + ")"
    return timepoint

@pytest.fixture()
def timepoint02_idSet(login_oldoperator, gns_idSet, cluster_idSet):
    """获取最新时间点"""
    file = open('D:\MyProject\Api-test\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['timepoint_url'])
    header = res['timepoint_headers']
    cookie = login_oldoperator
    datainfo = {"clusterId": cluster_idSet,
                "clusterVip": "10.2.12.76",
                "endTime": 1493596800000000,
                "gnsPath": gns_idSet,
                "count": 15,
                "jobStorageId": 1,
                "requestId": "",
                "startTime": 1491004800000000,
                "index": 0}
    # print(f'datainfo:{datainfo}')
    response = requests.get(url=url, headers=header, params=datainfo, verify=False, cookies=cookie).json()
    # print(f'response:{response}')
    return response['responseData']['data'][0]['timepoint']

@pytest.fixture()
def timepoint03_idSet(login_oldoperator, gns_idSet, cluster_idSet):
    """获取最新时间点的任务类型"""
    file = open('D:\MyProject\Api-test\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['timepoint_url'])
    header = res['timepoint_headers']
    cookie = login_oldoperator
    datainfo = {"clusterId": cluster_idSet,
                "clusterVip": "10.2.12.76",
                "endTime": 1493596800000000,
                "gnsPath": gns_idSet,
                "count": 15,
                "jobStorageId": 1,
                "requestId": "",
                "startTime": 1491004800000000,
                "index": 0}
    # print(f'datainfo:{datainfo}')
    response = requests.get(url=url, headers=header, params=datainfo, verify=False, cookies=cookie).json()
    # print(f'response:{response}')
    if response['responseData']['data'][0]['backupType'] == 1:
        return "完全备份"
    if response['responseData']['data'][0]['backupType'] == 2:
        return "增量备份"

@pytest.fixture()
def jobname_idSet(login_oldoperator, job_idSet):
    """获取恢复任务名"""
    file = open('D:\MyProject\Api-test\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['jobname_url'])
    header = res['jobname_headers']
    cookie = login_oldoperator
    datainfo = {"backupJobId": job_idSet,
                "backupJobName": "file1"
                }
    response = requests.get(url=url, headers=header, params=datainfo, verify=False, cookies=cookie).json()
    print(f'response:{response}')
    return response['responseData']['recoveryJobName']
