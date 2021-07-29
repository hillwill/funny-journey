import sys
# sys.path.append("D:\\6-0-Prepare_Job\\")
sys.path.append("/eisoo/CZB-Test/workspace/")
import yaml
import pytest
import allure
from urllib import parse
from common import common
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

@allure.title("新建指纹池成功！")
@pytest.mark.parametrize("fingerpool, expected",
                         [
                             ({"fpName": "zwc1",
                               "nodeNum": 1}, "success"),
                         ])
def test_Createfingerpool(login_operator, get_version, get_baseurl, fp_nodeIps, fingerpool, expected):
    file = open('/eisoo/CZB-Test/workspace/4-0-Prepare_Job/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    method = res['fingerpool_method']
    url = parse.urljoin(base_url, res['fingerpool_url'])
    referer = parse.urljoin(base_url, res['fingerpool_referer'])
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie,userId = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_operator
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}

    fingerpool["nodeIps"] = fp_nodeIps
    s = common.Webrequests()
    response = s.run_main(method, url, fingerpool, header, cookie)
    print(response)
    assert response['status'] == expected

@allure.title("新建指纹库成功！")
@pytest.mark.parametrize("flibinfo, expected",
                         [
                             ({"appType": 0,
                               "flName": "zwk1"}, "success"),
                             ({"appType": 1,
                               "flName": "zwk2"}, "success"),
                             ({"appType": 2,
                               "flName": "zwk3"}, "success"),
                         ])
def test_Createfingerlib(login_operator, get_baseurl, get_version, fp_Guid, flibinfo, expected):
    file = open('/eisoo/CZB-Test/workspace/4-0-Prepare_Job/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    url = parse.urljoin(base_url, res['flib_url'])
    referer = parse.urljoin(base_url, res['flib_referer'])
    method = res['flib_method']
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_operator
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    fpId, fpName = fp_Guid
    flibinfo["fpGuid"] = fpId
    flibinfo['fpName'] = fpName

    s = common.Webrequests()
    response = s.run_main(method, url, flibinfo, header, cookie)
    print(response)
    assert response['status'] == expected

if __name__== '___main__':
    pytest.main(["test_01_resource.py --Console_URL=base_url --Version=version"])
