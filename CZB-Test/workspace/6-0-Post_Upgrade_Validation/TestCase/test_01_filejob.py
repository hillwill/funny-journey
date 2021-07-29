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

@allure.title("发起文件增量备份任务成功！")
@pytest.mark.parametrize("jobinfo, expected",
                         [
                             ({"jobBackupType": 2,
                               "jobDesc": "",
                               "jobStatus": 4},"success"),
                         ])
def test_Runjob(login_operator, get_baseurl, get_version, get_clientip, get_filemd5, jobinfo, expected):
    file = open('/eisoo/CZB-Test/workspace/6-0-Post_Upgrade_Validation/TestData/config.yaml')
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
    get_filemd5
    sleep(60)

@allure.title("恢复文件备份任务成功!")
@pytest.mark.parametrize("jobinfo, expected",
                         [
                             ({"jobDataProduceType": 1,
                               "jobDesc": "",
                               "jobStorageId": "1",
                               "jobType": "eso_backupengine_fileengine"}, "success")
                         ])
def test_RunRestore(login_operator, login_sadmin, get_baseurl, get_version, get_clientip, cluster_idSet, jobinfo, expected):
    file = open('/eisoo/CZB-Test/workspace/6-0-Post_Upgrade_Validation/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    clientIP = get_clientip
    
    url = parse.urljoin(base_url, res['restore_job_url'])
    referer = parse.urljoin(base_url, res['restore_job_referer'])
    method = res['restore_job_method']

    if get_clientip == False:
        pytest.skip(msg='This test if only for file restore')
    elif version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_operator
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    
    clusterId, vip = cluster_idSet
    clientId, clientName = common.client_details_from_IP(base_url, version, login_sadmin, clientIP)
    clientIp = get_clientip
    gnsPath, BackupType, timestamp = common.get_last_timepoint(login_operator, base_url, version, cluster_idSet, 'file')
    timepoint = common.timestamptopoint(login_operator, base_url, version, cluster_idSet, 'file')
    jobinfo['clusterId'] = clusterId
    jobinfo['clusterVip'] = vip
    jobinfo['jobClientId'] = clientId
    jobinfo['jobCreatorId'] =  userId
    jobinfo['jobDestClientId'] = clientId
    jobinfo['jobDestClientIp'] = clientIp
    jobinfo['jobDestClientName'] = clientName
    jobinfo['jobId'] = common.jobId_from_jobName(base_url, version, login_operator, 'file')
    jobinfo['jobRelatedId'] = common.jobId_from_jobName(base_url, version, login_operator, 'file')
    jobinfo['jobName'] = common.get_restore_jobname(login_operator, base_url, version, 'file')
    dispPath = '[' + '"' + "%s" %timepoint + '"' + "," + '"/"' + ']'
    jobinfo['jobAdvParam'] = [{"key": "EEE_CUSTOM_SCRIPT", "value": "0"},
                              {"key": "EEE_LANFREE_OPEN_FC", "value": "0"},
                              {"key": "EEE_TIMEPOINT_USER_CHOOSE", "value": "%s" %(gnsPath)},
                              {"key": "EEE_RESTORE_GNS", "value": "%s" %(gnsPath)},
                              {"key": "EEE_IS_MOUNT_RESTORE", "value": "0"},
                              {"key": "EEE_IS_SINGLE_RESTORE", "value": "0"},
                              {"key": "EEE_RESTORE_REPLACE_STRATEGY", "value": "0"},
                              {"key": "EEE_DATA_WRITE_THREAD", "value": "8"},
                              {"key": "EEE_RESTORE_PATH", "value": ""},
                              {"key": "EEE_JOB_RUN_IMMEDIATELY", "value": "1"}]
    jobinfo['jobDataSource'] = [{"customer": "0",
                                 "dispPath": "%s" %dispPath,
                                 "fullPath": "%s" %gnsPath}] 
    print(url)
    print(f'jobinfo:{jobinfo}')
    print(header)
    print(cookie)

    s = common.Webrequests()
    response = s.run_main(method, url, jobinfo, header, cookie)
    print(response)
    assert response['status'] == expected
    sleep(20)

@allure.title("文件备份任务md5值对比结果：一致!")
def test_Diffmd5(diff_filemd5):
    md5 = diff_filemd5
    print(md5)
    print(diff_filemd5)
    assert md5 == ''

if __name__== '___main__':
    pytest.main(["test_01_filejob.py --Console_URL=base_url --Version=version --file_ClientIP=clientIP --file_ClientIP=clientIp --file_DataSource=fullpath"])
