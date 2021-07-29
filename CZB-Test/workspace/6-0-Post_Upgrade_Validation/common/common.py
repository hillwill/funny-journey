#!/usr/bin/env python
#*-*coding:utf-8*-*
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import json
import time
from time import sleep
from urllib import parse
import yaml

class Webrequests():
    def get(self,url,data,headers,cookie):
        try:
            r = requests.get(url,params=data,headers=headers,verify=False,cookies=cookie)
            json_r = r.json()
            return json_r
        except BaseException as e:
            print("请求失败！",str(e))
    def get_file(self,url,data,headers,cookie):
        try:
            r = requests.get(url,params=data,headers=headers,verify=False,cookies=cookie,stream=True)
            return r
        except BaseException as e:
            print("请求失败！",str(e))
    def post_data(self,url,data,headers):
        try:
            r = requests.post(url,data=data,headers=headers)
            r.encoding = 'utf-8'
            json_r = r.json()
            print("Test执行结果：",json_r)
            return json_r
        except BaseException as e:
            print("请求失败！",str(e))
    def post(self,url,data,headers,cookie):
        try:
            r = requests.post(url=url,json=data,headers=headers,verify=False,cookies=cookie)
            json_r = r.json()
            return json_r
        except BaseException as e:
            print("请求失败！",str(e))
    def put(self,url,data,headers,cookie):
        try:
            r = requests.put(url=url,json=data,headers=headers,verify=False,cookies=cookie)
            json_r = r.json()
            return json_r
        except BaseException as e:
            print("请求失败！", str(e))
    def delete(self,url,data,headers,cookie):
        try:
            r = requests.delete(url=url,json=data,headers=headers,verify=False,cookies=cookie)
            json_r = r.json()
            return json_r
        except BaseException as e:
            print("请求失败！",str(e))
    def post_file(self,url,data,headers,cookie):
        try:
            r = requests.post(url=url,files=data,headers=headers,cookies=cookie,verify=False)
            json_r = r.json()
            return json_r
        except BaseException as e:
            print("请求失败！",str(e))

    def run_main(self,method,url,data,headers,cookie):
        result = None
        if method == 'post_data':
            result = self.post_data(url,data,headers,cookie)
        elif method == 'get':
            result = self.get(url,data,headers,cookie)
        elif method == 'get_file':
            result = self.get_file(url,data,headers,cookie)
        elif method == 'post':
            result = self.post(url, data, headers,cookie)
        elif method == 'put':
            result = self.put(url, data, headers,cookie)
        elif method == 'delete':
            result = self.delete(url, data, headers,cookie)
        elif method == 'post_file':
            result = self.post_file(url, data, headers, cookie)
        else:
            print("method值错误！！！")
        return result

def jobId_from_jobName(get_baseurl, get_version, login_operator, jobName):
    """获取指定任务的id"""
    file = open('/eisoo/CZB-Test/workspace/6-0-Post_Upgrade_Validation/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    url = parse.urljoin(base_url, res['jobId_url'])
    referer = parse.urljoin(base_url, res['jobId_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_operator
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
        if jobId_from_jobName_response['responseData']['data'][i]['jobName'] == jobName:
            jobId = jobId_from_jobName_response['responseData']['data'][i]['jobId']
            return jobId
        i += 1

def client_details_from_IP(get_baseurl, get_version, login_sadmin, clientIP):
    """通过客户端IP获取客户端的其他信息"""
    file = open('/eisoo/CZB-Test/workspace/6-0-Post_Upgrade_Validation/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    url = parse.urljoin(base_url, res['client_idSet_url'])
    referer = parse.urljoin(base_url, res['client_idSet_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie = login_sadmin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, csrftoken = login_sadmin
        csrftoken = cookie['csrftoken']
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    datainfo = {"clientIsBuildin": "false",
                "count": 15,
                "filter": "",
                "includeSubUser": "true",
                "index": 0}
    print(url)
    print(datainfo)
    print(header)

    client_details_from_IP_response = requests.get(url, params=datainfo, headers=header, verify=False, cookies=cookie).json()
    sleep(1)
    print(client_details_from_IP_response)
    totalNum = client_details_from_IP_response['responseData']['totalNum']
    
    i = 0
    while i < totalNum:
        if client_details_from_IP_response['responseData']['data'][i]['clientIp'] == clientIP:
            clientId = client_details_from_IP_response['responseData']['data'][i]['clientId']
            clientName = client_details_from_IP_response['responseData']['data'][i]['clientName']
            print(clientId, clientName)
            return clientId, clientName
        i += 1

def get_job_cid(login_operator, get_baseurl, get_version, jobName):
    """获取指定任务的cid"""
    file = open("/eisoo/CZB-Test/workspace/6-0-Post_Upgrade_Validation/TestData/config.yaml")
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    url = parse.urljoin(base_url, res['job_cid_url'])
    referer = parse.urljoin(base_url, res['job_cid_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_operator
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    datainfo = {"index": 0,
                "count": 15}
    print(url)
    print(header)
    print(datainfo)

    job_cid_response = requests.get(url, params=datainfo, headers=header, verify=False, cookies=cookie).json()
    print(job_cid_response)
    totalNum = job_cid_response['responseData']['totalNum']
    i = 0
    while i < totalNum:
        if job_cid_response['responseData']['data'][i]['jobName'] == jobName:
            gnsPath = job_cid_response['responseData']['data'][i]['gnsPath']
            return gnsPath
        else:
            i += 1

def get_last_timepoint(login_operator, get_baseurl, get_version, cluster_idSet, jobName):
    """获取指定任务最新一次备份时间点"""
    file = open("/eisoo/CZB-Test/workspace/6-0-Post_Upgrade_Validation/TestData/config.yaml")
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    url = parse.urljoin(base_url, res['timepoint_url'])
    referer = parse.urljoin(base_url, res['timepoint_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_operator
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    jobcid = get_job_cid(login_operator, base_url, version, jobName)
    clusterId, clusterVip= cluster_idSet
    datainfo = {"clusterId": clusterId,
                "clusterVip": clusterVip,
                "count": 15,
                "endTime": 0,
                "gnsPath": jobcid,
                "index": 0,
                "jobStorageId": 1,
                "requestId": "",
                "startTime": 0}
    print(url)
    print(header)
    print(datainfo)

    timepoint_response = requests.get(url, params=datainfo, headers=header, verify=False, cookies=cookie).json()
    print(f'timepoint_response:{timepoint_response}')
    gnsPath = timepoint_response['responseData']['data'][0]['gnsPath']
    backupType = timepoint_response['responseData']['data'][0]['backupType']
    timepoint = timepoint_response['responseData']['data'][0]['timepoint']
    return gnsPath, backupType, timepoint

def get_vmwaretimepoint_subset(login_operator, get_baseurl, get_version, cluster_idSet, jobName):
    """获取指定vmware任务备份时间点的详细gns"""
    file = open("/eisoo/CZB-Test/workspace/6-0-Post_Upgrade_Validation/TestData/config.yaml")
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    url = parse.urljoin(base_url, res['timepoint_subset_url'])
    referer = parse.urljoin(base_url, res['timepoint_subset_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_operator
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    gnsPath, backupType, timepoint = get_last_timepoint(login_operator, base_url, version, cluster_idSet, jobName)
    clusterId, clusterVip= cluster_idSet
    datainfo = {"clusterId": clusterId,
                "clusterVip": clusterVip,
                "gnsPath": gnsPath,
                "jobStorageId": 1,
                "index": 0,
                "count": 100,
                "requestId": "",
                "engineType": 1002,
                "jobType": "eso_backupengine_vmwareengine"}
    print(url)
    print(header)
    print(datainfo)
    response = requests.post(url, data=datainfo, headers=header, verify=False, cookies=cookie).json()
    print(response)
    expandedFlag = response['responseData']['data'][0]['expandedFlag']
    gnsPath = response['responseData']['data'][0]['gnsPath']
    displayName = response['responseData']['data'][0]['displayName']
    print(expandedFlag)
    print(gnsPath)
    print(displayName)

    dpName = []
    dpName.append(displayName)
    num = 0
    while expandedFlag == True:
        datainfo['gnsPath'] = gnsPath
        
        response = requests.post(url, data=datainfo, headers=header, verify=False, cookies=cookie).json()
        print(response)
        expandedFlag = response['responseData']['data'][0]['expandedFlag']
        gnsPath = response['responseData']['data'][0]['gnsPath']
        displayName = response['responseData']['data'][0]['displayName']
        dpName.append(displayName)
        print(expandedFlag)
        print(gnsPath)
        print(displayName)
        num += 1
    else:
        return gnsPath, dpName, num

def timestamptopoint(login_operator, get_baseurl, get_version, cluster_idSet, jobName):
    """将指定时间戳转换成备份时间点"""
    gnsPath, backupType, timestamp = get_last_timepoint(login_operator, get_baseurl, get_version, cluster_idSet, jobName)
    print(f'timestamp:{timestamp}')
    timestamp_ten = timestamp / 1000000
    print(timestamp_ten)
    timearray = time.localtime(timestamp_ten)
    print(timearray)
    lasttime = time.strftime("%Y-%m-%d %H:%M:%S", timearray)
    print(lasttime)

    if backupType == 1:
        timepoint = lasttime +"(" + "完全备份" + ")"
    elif backupType == 2:
        timepoint = lasttime +"(" + "增量备份" + ")"
    elif backupType == 5:
        timepoint = lasttime + "(" + "永久增量备份" + ")"
    else:
        return False
    return timepoint

def get_restore_jobname(login_operator, get_baseurl, get_version, jobName):
    """获取指定任务的恢复任务名"""
    file = open("/eisoo/CZB-Test/workspace/6-0-Post_Upgrade_Validation/TestData/config.yaml")
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    jobId = jobId_from_jobName(base_url, version, login_operator, jobName)

    url = parse.urljoin(base_url, res['restore_jobname_url'])
    referer = parse.urljoin(base_url, res['restore_jobname_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_operator
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    datainfo = {"backupJobId": "%s" %(jobId),
                "backupJobName": "%s" %jobName}
    print(url)
    print(header)
    print(datainfo)

    restore_jobname_response = requests.get(url, params=datainfo, headers=header, verify=False, cookies=cookie).json()
    print(restore_jobname_response)
    recoveryJobName = restore_jobname_response['responseData']['recoveryJobName']
    return recoveryJobName
