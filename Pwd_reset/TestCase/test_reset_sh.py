#!/usr/bin/env python
#*-*coding:utf-8*-*
import sys
sys.path.append("D:\workspace\Pwd_reset")
import yaml
import pytest
import allure
from urllib import parse
from common import common
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

@allure.title("修改admin密码成功！修改后密码：eisoo.com123")
@pytest.mark.parametrize("resetadmin, expected",
                         [
                             ({"isEnc": "true",
                               "oldUserPass": "qH5DuXEgWFTKXofaeAygzigibB7ujOXbiotgvNvw9gy2ia3DIVBz/0e4b2o8OY7IP7xiJo96sIkmwVND1nvNSJre5x4M+ucAIaG3ZKFihNpmx+UkKn8r6Uidgz46PUuiOqYceGKoUSNavx4XEjNr3Pq+P1xQQKTvErtdr9vrRiI=",
                               "repeatUserPass": "rLbS6j09h7zIrX9WU5DqnKtns56HvV+GNxXKMb4+GXbS6P/OTv+BAyS8SpMkqTtdhvxLnvH+2jabwq6naVFP+7L9m5Ny0D8743SsQVKUYgnQq5cjUUqHlwgzbkWVZuMVaiDhen0BOFVQOpBxQGU2hOgq/hCNXbmXhecxh9fgruY=",
                               "userPass": "rLbS6j09h7zIrX9WU5DqnKtns56HvV+GNxXKMb4+GXbS6P/OTv+BAyS8SpMkqTtdhvxLnvH+2jabwq6naVFP+7L9m5Ny0D8743SsQVKUYgnQq5cjUUqHlwgzbkWVZuMVaiDhen0BOFVQOpBxQGU2hOgq/hCNXbmXhecxh9fgruY="}, "success"),
                         ])
def test_reset_admin_once(sh_login_admin, resetadmin, expected):
    file = open('D:\workspace\Pwd_reset\TestData\config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)

    # 获取修改密码需要的参数：method、header、resetadmin、cookie、url
    method = res['reset_method']
    cookie = sh_login_admin.cookies
    userId = sh_login_admin.cookies['userId']
    referer = res['sh_reset_headers']['Referer']
    csrftoken = sh_login_admin.cookies['csrftoken']
    header = {"referer": "%s" % (referer),
              "x-csrftoken": "%s" % (csrftoken)}

    resetadmin['userId'] = userId
    url = parse.urljoin(res['sh_base_url'], res['reset_url']).format(userId)

    # 修改密码为eisoo.com123
    s = common.Webrequests()
    response = s.run_main(method, url, resetadmin, header, cookie)
    print(response)
    assert response['status'] == expected

@allure.title("修改admin密码成功！修改后密码：EISOO.COM123")
@pytest.mark.parametrize("resetadmin, expected",
                         [
                             ({"isEnc": "true",
                               "oldUserPass": "rLbS6j09h7zIrX9WU5DqnKtns56HvV+GNxXKMb4+GXbS6P/OTv+BAyS8SpMkqTtdhvxLnvH+2jabwq6naVFP+7L9m5Ny0D8743SsQVKUYgnQq5cjUUqHlwgzbkWVZuMVaiDhen0BOFVQOpBxQGU2hOgq/hCNXbmXhecxh9fgruY=",
                               "repeatUserPass": "qH5DuXEgWFTKXofaeAygzigibB7ujOXbiotgvNvw9gy2ia3DIVBz/0e4b2o8OY7IP7xiJo96sIkmwVND1nvNSJre5x4M+ucAIaG3ZKFihNpmx+UkKn8r6Uidgz46PUuiOqYceGKoUSNavx4XEjNr3Pq+P1xQQKTvErtdr9vrRiI=",
                               "userPass": "qH5DuXEgWFTKXofaeAygzigibB7ujOXbiotgvNvw9gy2ia3DIVBz/0e4b2o8OY7IP7xiJo96sIkmwVND1nvNSJre5x4M+ucAIaG3ZKFihNpmx+UkKn8r6Uidgz46PUuiOqYceGKoUSNavx4XEjNr3Pq+P1xQQKTvErtdr9vrRiI="}, "success"),
                         ])
def test_reset_admin_twice(resetadmin, expected):
    file = open('D:\workspace\Pwd_reset\TestData\config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)

    # 获取临时cookies
    url = parse.urljoin(res['sh_base_url'], res['login_url'])
    print(f'url:{url}')
    header = res['sh_login_headers']
    print(f'header:{header}')
    logininfo = {"userName": "admin",
                 "userPass": "rLbS6j09h7zIrX9WU5DqnKtns56HvV+GNxXKMb4+GXbS6P/OTv+BAyS8SpMkqTtdhvxLnvH+2jabwq6naVFP+7L9m5Ny0D8743SsQVKUYgnQq5cjUUqHlwgzbkWVZuMVaiDhen0BOFVQOpBxQGU2hOgq/hCNXbmXhecxh9fgruY=",
                 # eisoo.com123
                 "validPwdExpire": "true",
                 "isEnc": "true"}
    sh_login_response = requests.post(url, headers=header, json=logininfo, verify=False)
    print(sh_login_response)

    # 获取修改密码需要的参数：method、header、resetadmin、cookie、url
    method = res['reset_method']
    cookie = sh_login_response.cookies
    userId = sh_login_response.cookies['userId']
    referer = res['sh_reset_headers']['Referer']
    csrftoken = sh_login_response.cookies['csrftoken']
    reset_header = {"referer": "%s" % (referer),
              "x-csrftoken": "%s" % (csrftoken)}

    resetadmin['userId'] = userId
    reset_url = parse.urljoin(res['sh_base_url'], res['reset_url']).format(userId)


    # 修改密码为EISOO.COM123
    s = common.Webrequests()
    response = s.run_main(method, reset_url, resetadmin, reset_header, cookie)
    print(response)
    assert response['status'] == expected

@allure.title("修改sadmin密码成功！修改后密码：eisoo.com123")
@pytest.mark.parametrize("resetsadmin, expected",
                         [
                             ({"isEnc": "true",
                               "oldUserPass": "qH5DuXEgWFTKXofaeAygzigibB7ujOXbiotgvNvw9gy2ia3DIVBz/0e4b2o8OY7IP7xiJo96sIkmwVND1nvNSJre5x4M+ucAIaG3ZKFihNpmx+UkKn8r6Uidgz46PUuiOqYceGKoUSNavx4XEjNr3Pq+P1xQQKTvErtdr9vrRiI=",
                               "repeatUserPass": "rLbS6j09h7zIrX9WU5DqnKtns56HvV+GNxXKMb4+GXbS6P/OTv+BAyS8SpMkqTtdhvxLnvH+2jabwq6naVFP+7L9m5Ny0D8743SsQVKUYgnQq5cjUUqHlwgzbkWVZuMVaiDhen0BOFVQOpBxQGU2hOgq/hCNXbmXhecxh9fgruY=",
                               "userPass": "rLbS6j09h7zIrX9WU5DqnKtns56HvV+GNxXKMb4+GXbS6P/OTv+BAyS8SpMkqTtdhvxLnvH+2jabwq6naVFP+7L9m5Ny0D8743SsQVKUYgnQq5cjUUqHlwgzbkWVZuMVaiDhen0BOFVQOpBxQGU2hOgq/hCNXbmXhecxh9fgruY="}, "success"),
                         ])
def test_reset_sadmin_once(sh_login_sadmin, resetsadmin, expected):
    file = open('D:\workspace\Pwd_reset\TestData\config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)

    # 获取修改密码需要的参数：method、header、resetsadmin、cookie、url
    method = res['reset_method']
    cookie = sh_login_sadmin.cookies
    userId = sh_login_sadmin.cookies['userId']
    referer = res['sh_reset_headers']['Referer']
    csrftoken = sh_login_sadmin.cookies['csrftoken']
    header = {"referer": "%s" % (referer),
              "x-csrftoken": "%s" % (csrftoken)}

    resetsadmin['userId'] = userId
    url = parse.urljoin(res['sh_base_url'], res['reset_url']).format(userId)


    # 修改密码为eisoo.com123
    s = common.Webrequests()
    response = s.run_main(method, url, resetsadmin, header, cookie)
    print(response)
    assert response['status'] == expected

@allure.title("修改sadmin密码成功！修改后密码：EISOO.COM123")
@pytest.mark.parametrize("resetsadmin, expected",
                         [
                             ({"isEnc": "true",
                               "oldUserPass": "rLbS6j09h7zIrX9WU5DqnKtns56HvV+GNxXKMb4+GXbS6P/OTv+BAyS8SpMkqTtdhvxLnvH+2jabwq6naVFP+7L9m5Ny0D8743SsQVKUYgnQq5cjUUqHlwgzbkWVZuMVaiDhen0BOFVQOpBxQGU2hOgq/hCNXbmXhecxh9fgruY=",
                               "repeatUserPass": "qH5DuXEgWFTKXofaeAygzigibB7ujOXbiotgvNvw9gy2ia3DIVBz/0e4b2o8OY7IP7xiJo96sIkmwVND1nvNSJre5x4M+ucAIaG3ZKFihNpmx+UkKn8r6Uidgz46PUuiOqYceGKoUSNavx4XEjNr3Pq+P1xQQKTvErtdr9vrRiI=",
                               "userPass": "qH5DuXEgWFTKXofaeAygzigibB7ujOXbiotgvNvw9gy2ia3DIVBz/0e4b2o8OY7IP7xiJo96sIkmwVND1nvNSJre5x4M+ucAIaG3ZKFihNpmx+UkKn8r6Uidgz46PUuiOqYceGKoUSNavx4XEjNr3Pq+P1xQQKTvErtdr9vrRiI="}, "success"),
                         ])
def test_reset_sadmin_twice(resetsadmin, expected):
    file = open('D:\workspace\Pwd_reset\TestData\config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)

    # 获取临时cookies
    url = parse.urljoin(res['sh_base_url'], res['login_url'])
    print(f'url:{url}')
    header = res['sh_login_headers']
    print(f'header:{header}')
    logininfo = {"userName": "sadmin",
                 "userPass": "rLbS6j09h7zIrX9WU5DqnKtns56HvV+GNxXKMb4+GXbS6P/OTv+BAyS8SpMkqTtdhvxLnvH+2jabwq6naVFP+7L9m5Ny0D8743SsQVKUYgnQq5cjUUqHlwgzbkWVZuMVaiDhen0BOFVQOpBxQGU2hOgq/hCNXbmXhecxh9fgruY=",
                 # eisoo.com123
                 "validPwdExpire": "true",
                 "isEnc": "true"}
    sh_login_response = requests.post(url, headers=header, json=logininfo, verify=False)
    print(sh_login_response)

    # 获取修改密码需要的参数：method、header、resetsadmin、cookie、url
    method = res['reset_method']
    cookie = sh_login_response.cookies
    userId = sh_login_response.cookies['userId']
    referer = res['sh_reset_headers']['Referer']
    csrftoken = sh_login_response.cookies['csrftoken']
    reset_header = {"referer": "%s" % (referer),
              "x-csrftoken": "%s" % (csrftoken)}

    resetsadmin['userId'] = userId
    reset_url = parse.urljoin(res['sh_base_url'], res['reset_url']).format(userId)

    # 修改密码为EISOO.COM123
    s = common.Webrequests()
    response = s.run_main(method, reset_url, resetsadmin, reset_header, cookie)
    print(response)
    assert response['status'] == expected

@allure.title("修改操作员密码成功！修改后密码：eisoo.com123")
@pytest.mark.parametrize("resetoperator, expected",
                         [
                             ({"isEnc": "true",
                               "oldUserPass": "qH5DuXEgWFTKXofaeAygzigibB7ujOXbiotgvNvw9gy2ia3DIVBz/0e4b2o8OY7IP7xiJo96sIkmwVND1nvNSJre5x4M+ucAIaG3ZKFihNpmx+UkKn8r6Uidgz46PUuiOqYceGKoUSNavx4XEjNr3Pq+P1xQQKTvErtdr9vrRiI=",
                               "repeatUserPass": "rLbS6j09h7zIrX9WU5DqnKtns56HvV+GNxXKMb4+GXbS6P/OTv+BAyS8SpMkqTtdhvxLnvH+2jabwq6naVFP+7L9m5Ny0D8743SsQVKUYgnQq5cjUUqHlwgzbkWVZuMVaiDhen0BOFVQOpBxQGU2hOgq/hCNXbmXhecxh9fgruY=",
                               "userPass": "rLbS6j09h7zIrX9WU5DqnKtns56HvV+GNxXKMb4+GXbS6P/OTv+BAyS8SpMkqTtdhvxLnvH+2jabwq6naVFP+7L9m5Ny0D8743SsQVKUYgnQq5cjUUqHlwgzbkWVZuMVaiDhen0BOFVQOpBxQGU2hOgq/hCNXbmXhecxh9fgruY="}, "success"),
                         ])
def test_reset_operator_once(sh_login_operator, resetoperator, expected):
    file = open('D:\workspace\Pwd_reset\TestData\config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)

    # 获取修改密码需要的参数：method、header、resetsadmin、cookie、url
    method = res['reset_method']
    cookie = sh_login_operator.cookies
    userId = sh_login_operator.cookies['userId']
    referer = res['sh_reset_headers']['Referer']
    csrftoken = sh_login_operator.cookies['csrftoken']
    header = {"referer": "%s" % (referer),
              "x-csrftoken": "%s" % (csrftoken)}

    resetoperator['userId'] = userId
    url = parse.urljoin(res['sh_base_url'], res['reset_url']).format(userId)


    # 修改密码为eisoo.com123
    s = common.Webrequests()
    response = s.run_main(method, url, resetoperator, header, cookie)
    print(response)
    assert response['status'] == expected

@allure.title("修改sadmin密码成功！修改后密码：EISOO.COM123")
@pytest.mark.parametrize("resetoperator, expected",
                         [
                             ({"isEnc": "true",
                               "oldUserPass": "rLbS6j09h7zIrX9WU5DqnKtns56HvV+GNxXKMb4+GXbS6P/OTv+BAyS8SpMkqTtdhvxLnvH+2jabwq6naVFP+7L9m5Ny0D8743SsQVKUYgnQq5cjUUqHlwgzbkWVZuMVaiDhen0BOFVQOpBxQGU2hOgq/hCNXbmXhecxh9fgruY=",
                               "repeatUserPass": "qH5DuXEgWFTKXofaeAygzigibB7ujOXbiotgvNvw9gy2ia3DIVBz/0e4b2o8OY7IP7xiJo96sIkmwVND1nvNSJre5x4M+ucAIaG3ZKFihNpmx+UkKn8r6Uidgz46PUuiOqYceGKoUSNavx4XEjNr3Pq+P1xQQKTvErtdr9vrRiI=",
                               "userPass": "qH5DuXEgWFTKXofaeAygzigibB7ujOXbiotgvNvw9gy2ia3DIVBz/0e4b2o8OY7IP7xiJo96sIkmwVND1nvNSJre5x4M+ucAIaG3ZKFihNpmx+UkKn8r6Uidgz46PUuiOqYceGKoUSNavx4XEjNr3Pq+P1xQQKTvErtdr9vrRiI="}, "success"),
                         ])
def test_reset_operator_twice(resetoperator, expected):
    file = open('D:\workspace\Pwd_reset\TestData\config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)

    # 获取临时cookies
    url = parse.urljoin(res['sh_base_url'], res['login_url'])
    print(f'url:{url}')
    header = res['sh_login_headers']
    print(f'header:{header}')
    logininfo = {"userName": "eisoo",
                 "userPass": "rLbS6j09h7zIrX9WU5DqnKtns56HvV+GNxXKMb4+GXbS6P/OTv+BAyS8SpMkqTtdhvxLnvH+2jabwq6naVFP+7L9m5Ny0D8743SsQVKUYgnQq5cjUUqHlwgzbkWVZuMVaiDhen0BOFVQOpBxQGU2hOgq/hCNXbmXhecxh9fgruY=",
                 # eisoo.com123
                 "validPwdExpire": "true",
                 "isEnc": "true"}
    sh_login_response = requests.post(url, headers=header, json=logininfo, verify=False)
    print(sh_login_response)

    # 获取修改密码需要的参数：method、header、resetsadmin、cookie、url
    method = res['reset_method']
    cookie = sh_login_response.cookies
    userId = sh_login_response.cookies['userId']
    referer = res['sh_reset_headers']['Referer']
    csrftoken = sh_login_response.cookies['csrftoken']
    reset_header = {"referer": "%s" % (referer),
              "x-csrftoken": "%s" % (csrftoken)}

    resetoperator['userId'] = userId
    reset_url = parse.urljoin(res['sh_base_url'], res['reset_url']).format(userId)

    # 修改密码为EISOO.COM123
    s = common.Webrequests()
    response = s.run_main(method, reset_url, resetoperator, reset_header, cookie)
    print(response)
    assert response['status'] == expected

if __name__ == '__main__':
    pytest.main(["test_reset.py"])
