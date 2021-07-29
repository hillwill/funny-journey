import sys
sys.path.append("/eisoo/CZB-Test/workspace/")
import yaml
import pytest
import allure
from urllib import parse
from common import common
import requests
from time import sleep
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

@allure.title("分配文件任务的客户端成功！")
@pytest.mark.parametrize("clientinfo, expected",
                         [
                             ({"clientIsBuildin": "false",
                               "nodeIp": "",
                               "requestId": "",
                               "userNames": ["test"]}, "success"),
                         ])
def test_client(login_sadmin, get_baseurl, get_version, get_clientip, clientinfo, expected):
    file = open('/eisoo/CZB-Test/workspace/4-0-Prepare_Job/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    url = parse.urljoin(base_url, res['client_url'])
    referer = parse.urljoin(base_url, res['client_referer'])
    method = res['client_method']
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie = login_sadmin
        header = {"referer": "%s" % (referer)}
    else:
        cookie, csrftoken = login_sadmin
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}

    clientIP = get_clientip
    clientId, clientName = common.client_details_from_IP(base_url, version, login_sadmin, clientIP)
    clientinfo["ids"] = ["%s" %clientId]
    print(url)
    print(header)
    print(method)
    print(clientinfo)

    s = common.Webrequests()
    response = s.run_main(method, url, clientinfo, header, cookie)
    print(response)
    print(response['responseData']['requestId'])
    assert response['status'] == expected

@allure.title("创建备份任务成功！")
@pytest.mark.parametrize("jobinfo, expected",
                         [
                             ({"filterDatas":
                                   [{"filterType": 1, "filterMode": 1, "content": []},
                                    {"filterType": 2, "filterMode": 1, "content": []},
                                    {"filterType": 3, "filterMode": 1, "content": {"filterTypes": [], "other": []}},
                                    {"filterType": 4, "filterMode": 1, "content": {}}],
                               "jobDatabaseRunUsername": "",
                               "jobDesc": "",
                               "jobName": "file",
                               "jobPlanId": "",
                               "jobStorageId": "1",
                               "jobType": "eso_backupengine_fileengine"}, "success"),
                         ])
def test_Createjob(login_sadmin, login_operator, get_baseurl, get_version, get_clientip, get_fullpath, get_filedispath, jobinfo, expected):
    file = open('/eisoo/CZB-Test/workspace/4-0-Prepare_Job/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    url = parse.urljoin(base_url, res['job_url'])
    referer = parse.urljoin(base_url, res['job_referer'])
    method = res['job_method']
    
    if get_clientip == False:
        pytest.skip(msg='This test if only for file backup')
    elif version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_operator
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    clientIP = get_clientip
    clientId, clientName = common.client_details_from_IP(base_url, version, login_sadmin, clientIP)
    fullpath = get_fullpath
    clientIp = get_clientip
    #flibId = file_flib_idSet
    flibId = common.get_flib_idSet(base_url, version, login_operator, 0)
    jobinfo['jobClientId'] = clientId
    jobinfo['jobCreatorId'] = userId
    
    dispath = get_filedispath
    splice = '[' + '"%s(%s)"' %(clientName, clientIp) + "," + '"文件系统备份服务器"' + "," + '"/"'
    for i in range(len(dispath)):
        print(i)
        print(dispath[i])
        splice = splice + "," + '"%s"' %(dispath[i])
        i += 1
    splice = splice + ']'
    jobinfo['jobDataSource'] = [{"fullPath": "%s" %fullpath, 
                                 "dispPath": "%s" %splice,
                                 "customer": 0,
                                 "nodeType": 1001,
                                 "uuid": ""}]
    
    jobinfo['jobAdvParam'] = [{"key": "EEE_AUTO_RESTART", "value": "0"},
                              {"key": "EEE_PERMANENT_INCREMENT", "value": "1"},
                              {"key": "EEE_LANFREE_OPEN_FC", "value": "0"},
                              {"key": "EEE_LANFREE_CHANNEL_COUNT", "value": "1"},
                              {"key": "EEE_ENCRYPTION_XXXX", "value": "1"},
                              {"key": "EEE_DEDUP", "value": "1"},
                              {"key": "EEE_FLOW_CONTROL_NEW", "value": "0"},
                              {"key": "EEE_FLOW_CONTROL", "value": "1024"},
                              {"key": "EEE_CUSTOM_SCRIPT", "value": "0"},
                              {"key": "EEE_COMPRESS_ALGO_CHECKED", "value": "0"},
                              {"key": "EEE_AUTO_RESTART_COUNT", "value": "1"},
                              {"key": "EEE_AUTO_RESTART_INTERVAL", "value": "1"},
                              {"key": "EEE_ENCRYPT_ALGO", "value": "AES256"},
                              {"key": "EEE_DEDUP_POOL_ID", "value": "%s" %flibId},
                              {"key": "EEE_BACKUP_CHANNEL_CONFS", "value": "0"},
                              {"key": "EEE_TRAVERSAL_THREAD", "value": "20"},
                              {"key": "EEE_READER_THREAD", "value": "1"},
                              {"key": "EEE_JOB_RUN_IMMEDIATELY", "value": "0"}]
    print(url)
    print(jobinfo)
    print(header)
    print(cookie)

    s = common.Webrequests()
    response = s.run_main(method, url, jobinfo, header, cookie)
    print(response)
    assert response['status'] == expected

@allure.title("发起备份任务成功！")
@pytest.mark.parametrize("jobinfo, expected",
                         [
                             ({"jobBackupType": 1,
                               "jobDesc": "",
                               "jobStatus": 4},"success"),
                             #({"jobBackupType": 2,
                             #  "jobDesc": "",
                             #  "jobStatus": 4},"success"),
                         ])
def test_Runjob(login_operator, get_baseurl, get_version, get_clientip, jobinfo, expected):
    file = open('/eisoo/CZB-Test/workspace/4-0-Prepare_Job/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    jobId = common.jobId_from_jobName(base_url, version, login_operator, 'file')

    url = parse.urljoin(base_url, res['runjob_url']).format(jobId)
    referer = parse.urljoin(base_url, res['runjob_referer'])
    method = res['runjob_method']
    
    if get_clientip == False:
        pytest.skip(msg='This test if only for file backup')
    elif version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_operator
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    jobinfo['jobId'] = jobId
    print(url)
    print(jobinfo)
    print(header)
    print(cookie)

    s = common.Webrequests()
    response = s.run_main(method, url, jobinfo, header, cookie)
    print(response)
    assert response['status'] == expected
    sleep(30)

if __name__== '___main__':
    pytest.main(["test_02_filejob.py --Console_URL=base_url --Version=version --file_ClientIP=clientIp --file_DataSource=fullpath"])
