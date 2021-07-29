#!/usr/bin/env python
#*-*coding:utf-8*-*
import requests
from urllib import parse
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import yaml
import json
from time import sleep

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

def get_flib_idSet(get_baseurl, get_version, login_operator, flibType):
    """获取指定类型的指纹库ID"""
    """0代表其它类型"""
    """1代表数据库类型"""
    """2代表虚拟化类型"""
    file = open('/eisoo/CZB-Test/workspace/4-0-Prepare_Job/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    url = parse.urljoin(base_url, res['flib_idSet_url'])
    referer = parse.urljoin(base_url, res['flib_idSet_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_operator
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    datainfo = {"count": 8,
                "index": 0,
                "jobType": "eso_backupengine_fileengine"}
    print(url)
    print(header)
    print(datainfo)

    flib_idSet_response = requests.get(url, params=datainfo, headers=header, verify=False, cookies=cookie).json()
    print(flib_idSet_response)
    totalNum = flib_idSet_response['responseData']['totalNum']
    i = 0
    while i < totalNum:
        if flib_idSet_response['responseData']['data'][i]['fpAppType'] == flibType:
            return flib_idSet_response['responseData']['data'][i]['fpGuid']
        else:
            i += 1

def jobId_from_jobName(get_baseurl, get_version, login_operator, jobName):
    """获取指定任务的id"""
    file = open('/eisoo/CZB-Test/workspace/4-0-Prepare_Job/TestData/config.yaml')
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
    file = open('/eisoo/CZB-Test/workspace/4-0-Prepare_Job/TestData/config.yaml')
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
