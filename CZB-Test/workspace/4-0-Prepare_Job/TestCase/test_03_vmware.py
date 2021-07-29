import sys
# sys.path.append("D:\\6-0-Prepare_Job\\")
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

@allure.title("创建vmware虚拟化平台成功！")
@pytest.mark.parametrize("vmwareinfo, expected",
                         [
                             ({"clientType": 15,
                               "engineType": 1001,
                               "platformCustomer": "{}",
                               "type": "3"}, "success"),
                         ])
def test_Create_vmwareplatform(login_operator, get_baseurl, get_version, get_vmwareip, get_vmwareusername, get_vmwarepassword, platform_verify, vmwareinfo, expected):
    file = open('/eisoo/CZB-Test/workspace/4-0-Prepare_Job/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    url = parse.urljoin(base_url, res['vmware_url'])
    referer = parse.urljoin(base_url, res['vmware_referer'])
    method = res['vmware_method']
    print(get_vmwareip)
    if get_vmwareip == False:
        pytest.skip(msg='This test if only for vmware backup')
    elif version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_operator
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    vmwareinfo['ip'] = get_vmwareip
    vmwareinfo['name'] = get_vmwareip
    vmwareinfo['username'] = get_vmwareusername
    vmwareinfo['password'] = get_vmwarepassword
    if version in ('7.0.14.0'):
        # 针对7.0.14版本新增的平台证书验证
        vmwareinfo['verification'] = platform_verify

    s = common.Webrequests()
    response = s.run_main(method, url, vmwareinfo, header, cookie)
    print(response)
    assert response['status'] == expected

@allure.title("创建VMware定时备份任务成功！")
@pytest.mark.parametrize("jobinfo, expected",
                         [
                             ({"jobDesc": "",
                               "jobName": "vmware",
                               "jobPlanId": "",
                               "jobStorageId": "1",
                               "jobType": "eso_backupengine_vmwareengine"}, "success"),
                         ])
def test_Createjob(login_operator, get_baseurl, get_version, get_vmwareip, platform_details_from_IP, vmwarepath_from_search, get_Builtin_Client_Id, jobinfo, expected):
    file = open('/eisoo/CZB-Test/workspace/4-0-Prepare_Job/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version

    url = parse.urljoin(base_url, res['job_url'])
    referer = parse.urljoin(base_url, res['job_referer'])
    method = res['job_method']

    if get_vmwareip == False:
        pytest.skip(msg='This test if only for vmware backup')
    elif version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_operator
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    
    builtin_clientId = get_Builtin_Client_Id
    fullpath, dispath, nodeType, customer, uuid = vmwarepath_from_search
    jobVplatformIp, jobVplatformName, jobVplatformId, version = platform_details_from_IP
    flibId = common.get_flib_idSet(base_url, version, login_operator, 2)
    
    jobinfo['jobClientId'] = builtin_clientId
    jobinfo['jobCreatorId'] = userId
    jobinfo['jobVplatformId'] = "%s" %jobVplatformId
    jobinfo['jobVplatformIp'] = "%s" %jobVplatformIp
    jobinfo['jobVplatformName'] = "%s" %jobVplatformName
    jobinfo['version'] = "%s" %version
    manyinfo = {"platformId": "%s" %jobVplatformId, "platformIp": "%s" %jobVplatformIp, "version": "%s" %version, "platformName": "%s" %jobVplatformName}
    jobinfo['jobDataSource'] = [{"fullPath": "%s" %fullpath,
                                 "dispPath": "%s" %dispath,
                                 "customer": "%s" %customer,
                                 "nodeType": nodeType,
                                 "uuid": "%s" %uuid}]
    jobinfo['jobAdvParam'] = [{"key": "EEE_CUSTOM_PARAM", "value": "{\"%s\" %manyinfo}"},
                              {"key": "EEE_VMWARE_CUSTOMER", "value": "host"},
                              {"key": "EEE_BACKUP_TRANSPORTMODE", "value": "nbd"},
                              {"key": "EEE_BACKUP_CBT", "value": "1"},
                              {"key": "EEE_BACKUP_QUEISCE", "value": "1"},
                              {"key": "EEE_IS_USE_THREAD", "value": "0"},
                              {"key": "EEE_USE_THREAD_NUM", "value": "2"},
                              {"key": "EEE_VM_AUTO_RESTART", "value": "0"},
                              {"key": "EEE_PERMANENT_INCREMENT", "value": "1"},
                              {"key": "EEE_ENCRYPTION_XXXX", "value": "1"},
                              {"key": "EEE_DEDUP", "value": "1"},
                              {"key": "EEE_COMPRESS_ALGO_CHECKED", "value": "0"},
                              {"key": "EEE_VM_AUTO_RESTART_COUNT", "value": "1"},
                              {"key": "EEE_VM_AUTO_RESTART_INTERVAL", "value": "1"},
                              {"key": "EEE_ENCRYPT_ALGO", "value": "AES256"},
                              {"key": "EEE_DEDUP_POOL_ID", "value": "%s" %flibId},
                              {"key": "EEE_FLOW_CONTROL_ENABLE", "value": "0"},
                              #{"key": "EEE_FLOW_CONTROL_CONFIG", "value": "0"},
                              {"key": "EEE_JOB_RUN_IMMEDIATELY", "value": "1"}]
    print(url)
    print(jobinfo)
    print(header)
    print(cookie)
    s = common.Webrequests()
    response = s.run_main(method, url, jobinfo, header, cookie)
    print(response)
    assert response['status'] == expected

@allure.title("发起vmware备份任务成功！")
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
    jobId = common.jobId_from_jobName(base_url, version, login_operator, 'vmware')

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
    pytest.main(["test_03_vmware.py --Console_URL=base_url --Version=version"])
