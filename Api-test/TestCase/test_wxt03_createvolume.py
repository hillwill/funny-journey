import sys
sys.path.append("D:\\MyProject\\Api-test")
from urllib import parse
import allure
import pytest
import requests
import yaml
from time import sleep
from common import common
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

@allure.title("创建ofs卷成功!")
@pytest.mark.parametrize("ofsinfo, expected",
                          [
                              ({"isEdit": "false",
                                "type": 1,
                                "desc": " ",
                                "name": "ofs",
                                "mountPath": "/mnt/sdb1",
                                "ngDialogId": "ngdialog2",
                                "pathSize": 105553780736,
                                "size": 53687091200,
                                "storageType": 0}, "success"),
                          ])

def test_create_ofs_volume(login_oldadmin,ofsinfo,expected,nodes_idSet):
    file = open('D:\\MyProject\\Api-test\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['createvolume_url'])
    header = res['createvolume_headers']
    method = res['createvolume_method']
    cookie = login_oldadmin
    nodeId = nodes_idSet
    ofsinfo['nodeId'] = nodeId
    s = common.Webrequests()
    response = s.run_main(method, url, ofsinfo, header, cookie)
    print(response)
    assert response['status'] == expected
    sleep(20)

@allure.title("创建meta卷成功!")
@pytest.mark.parametrize("metainfo, expected",
                          [
                              ({"isEdit": "false",
                                "type": 3,
                                "desc": " ",
                                "name": "meta",
                                "mountPath": "/mnt/sdb1",
                                "ngDialogId": "ngdialog2",
                                "pathSize": 51866689536,
                                "size": 10737418240,
                                "storageType": 0}, "success"),
                          ])

def test_create_meta_volume(login_oldadmin,metainfo,expected,nodes_idSet):
    file = open('D:\\MyProject\\Api-test\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['createvolume_url'])
    header = res['createvolume_headers']
    method = res['createvolume_method']
    cookie = login_oldadmin
    nodeId = nodes_idSet
    metainfo['nodeId'] = nodeId
    s = common.Webrequests()
    response = s.run_main(method, url, metainfo, header, cookie)
    print(response)
    assert response['status'] == expected
    sleep(20)

@allure.title("创建重删卷成功!")
@pytest.mark.parametrize("ddcinfo, expected",
                          [
                              ({"isEdit": "false",
                                "type": 2,
                                "desc": " ",
                                "name": "ddc",
                                "mountPath": "/mnt/sdb1",
                                "ngDialogId": "ngdialog2",
                                "pathSize": 41129271296,
                                "size": 10737418240,
                                "storageType": 0}, "success"),
                          ])

def test_create_ddc_volume(login_oldadmin,ddcinfo,expected,nodes_idSet):
    file = open('D:\\MyProject\\Api-test\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['createvolume_url'])
    header = res['createvolume_headers']
    method = res['createvolume_method']
    cookie = login_oldadmin
    nodeId = nodes_idSet
    ddcinfo['nodeId'] = nodeId
    s = common.Webrequests()
    response = s.run_main(method, url, ddcinfo, header, cookie)
    print(response)
    assert response['status'] == expected
    sleep(20)

if __name__ == "__main__":
    pytest.main(["test_wxt03_createvolume.py"])