#!/usr/bin/env python
#*-*coding:utf-8*-*
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import json

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
