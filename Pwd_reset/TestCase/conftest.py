import sys
sys.path.append('D:\workspace\Pwd_reset')
from urllib import parse
import pytest
import requests
import yaml
import datetime
from common import common
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

@pytest.fixture()
def sh_login_admin():
    """
    获取上海本部上线环境admin账户的cookies
    """
    file = open('D:\workspace\Pwd_reset\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['sh_base_url'], res['login_url'])
    print(f'url:{url}')
    header = res['sh_login_headers']
    print(f'header:{header}')
    logininfo = {"userName": "admin",
                 "userPass": "qH5DuXEgWFTKXofaeAygzigibB7ujOXbiotgvNvw9gy2ia3DIVBz/0e4b2o8OY7IP7xiJo96sIkmwVND1nvNSJre5x4M+ucAIaG3ZKFihNpmx+UkKn8r6Uidgz46PUuiOqYceGKoUSNavx4XEjNr3Pq+P1xQQKTvErtdr9vrRiI=",   #EISOO.COM123
                 "validPwdExpire": "true",
                 "isEnc": "true"}
    sh_login_response = requests.post(url, headers=header, json=logininfo, verify=False)
    print(f'sh_login_response:{sh_login_response}')
    assert sh_login_response.json()['status'] == 'success'
    return sh_login_response


@pytest.fixture()
def shidc_login_admin():
    """
    获取上海IDC上线环境admin账户的cookies
    """
    file = open('D:\workspace\Pwd_reset\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['shidc_base_url'], res['login_url'])
    header = res['shidc_login_headers']
    logininfo = {"userName": "admin",
                 "userPass": "qH5DuXEgWFTKXofaeAygzigibB7ujOXbiotgvNvw9gy2ia3DIVBz/0e4b2o8OY7IP7xiJo96sIkmwVND1nvNSJre5x4M+ucAIaG3ZKFihNpmx+UkKn8r6Uidgz46PUuiOqYceGKoUSNavx4XEjNr3Pq+P1xQQKTvErtdr9vrRiI=",   #EISOO.COM123
                 "validPwdExpire": "true",
                 "isEnc": "true"}
    shidc_login_response = requests.post(url, headers=header, json=logininfo, verify=False)
    print(f'shidc_login_response:{shidc_login_response}')
    assert shidc_login_response.json()['status'] == 'success'
    return shidc_login_response

@pytest.fixture()
def sh_login_sadmin():
    """
    获取上海本部上线环境安全管理员账户的cookies
    """
    file = open('D:\workspace\Pwd_reset\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['sh_base_url'], res['login_url'])
    header = res['sh_login_headers']
    logininfo = {"userName": "sadmin",
                 "userPass": "qH5DuXEgWFTKXofaeAygzigibB7ujOXbiotgvNvw9gy2ia3DIVBz/0e4b2o8OY7IP7xiJo96sIkmwVND1nvNSJre5x4M+ucAIaG3ZKFihNpmx+UkKn8r6Uidgz46PUuiOqYceGKoUSNavx4XEjNr3Pq+P1xQQKTvErtdr9vrRiI=",   #EISOO.COM123
                 "validPwdExpire": "true",
                 "isEnc": "true"}
    sh_login_response = requests.post(url, headers=header, json=logininfo, verify=False)
    print(f'sh_login_response:{sh_login_response}')
    assert sh_login_response.json()['status'] == 'success'
    return sh_login_response

@pytest.fixture()
def shidc_login_sadmin():
    """
    获取上海IDC上线环境安全管理员账户的cookies
    """
    file = open('D:\workspace\Pwd_reset\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['shidc_base_url'], res['login_url'])
    header = res['shidc_login_headers']
    logininfo={"userName":"sadmin",
               "userPass":"qH5DuXEgWFTKXofaeAygzigibB7ujOXbiotgvNvw9gy2ia3DIVBz/0e4b2o8OY7IP7xiJo96sIkmwVND1nvNSJre5x4M+ucAIaG3ZKFihNpmx+UkKn8r6Uidgz46PUuiOqYceGKoUSNavx4XEjNr3Pq+P1xQQKTvErtdr9vrRiI=",   #EISOO.COM123
               "validPwdExpire":"true",
               "isEnc":"true"}
    shidc_login_response = requests.post(url, headers=header, json=logininfo, verify=False)
    print(f'shidc_login_response:{shidc_login_response}')
    assert shidc_login_response.json()['status'] == 'success'
    return shidc_login_response

@pytest.fixture()
def sh_login_operator():
    """
    获取上海本部上线环境操作员账户的cookies
    """
    file = open('D:\workspace\Pwd_reset\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['sh_base_url'], res['login_url'])
    header = res['sh_login_headers']
    logininfo = {"userName": "eisoo",
                 "userPass": "qH5DuXEgWFTKXofaeAygzigibB7ujOXbiotgvNvw9gy2ia3DIVBz/0e4b2o8OY7IP7xiJo96sIkmwVND1nvNSJre5x4M+ucAIaG3ZKFihNpmx+UkKn8r6Uidgz46PUuiOqYceGKoUSNavx4XEjNr3Pq+P1xQQKTvErtdr9vrRiI=",   #EISOO.COM123
                 "validPwdExpire": "true",
                 "isEnc": "true"}
    sh_login_response = requests.post(url, headers=header, json=logininfo, verify=False)
    print(f'sh_login_response:{sh_login_response}')
    assert sh_login_response.json()['status'] == 'success'
    return sh_login_response

@pytest.fixture()
def shidc_login_operator():
    """
    获取上海IDC上线环境操作员账户的cookies
    """
    file = open('D:\workspace\Pwd_reset\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['shidc_base_url'], res['login_url'])
    header = res['shidc_login_headers']
    logininfo={"userName":"newer",
               "userPass":"qH5DuXEgWFTKXofaeAygzigibB7ujOXbiotgvNvw9gy2ia3DIVBz/0e4b2o8OY7IP7xiJo96sIkmwVND1nvNSJre5x4M+ucAIaG3ZKFihNpmx+UkKn8r6Uidgz46PUuiOqYceGKoUSNavx4XEjNr3Pq+P1xQQKTvErtdr9vrRiI=",   #EISOO.COM123
               "validPwdExpire":"true",
               "isEnc":"true"}
    shidc_login_response = requests.post(url, headers=header, json=logininfo, verify=False)
    print(f'shidc_login_response:{shidc_login_response}')
    assert shidc_login_response.json()['status'] == 'success'
    return shidc_login_response