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

@allure.title("发起Oracle定时增量备份任务成功！")
@pytest.mark.parametrize("jobinfo, expected",
                         [
                             ({"jobBackupType": 2,
                               "jobDesc": "",
                               "jobStatus": 4}, "success"),
                         ])
def test_Runjob(login_operator, get_baseurl, get_version, get_oracleclientip, jobinfo, expected):
    file = open('/eisoo/CZB-Test/workspace/6-0-Post_Upgrade_Validation/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    clientIP = get_oracleclientip
    jobId = common.jobId_from_jobName(base_url, version, login_operator, 'oracle')

    url = parse.urljoin(base_url, res['runjob_url']).format(jobId)
    referer = parse.urljoin(base_url, res['runjob_referer'])
    method = res['runjob_method']

    if clientIP == False:
        pytest.skip(msg='This test if only for oracle backup')
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
    sleep(100)

@allure.title("恢复oracle备份任务成功!")
@pytest.mark.parametrize("jobinfo, expected",
                         [
                             ({"clientType": 1,
                               "jobDataProduceType": 1,
                               "jobDesc": "",
                               "jobStorageId": "1",
                               "jobType": "eso_backupengine_oracleengine"}, "success")
                         ])
def test_RunRestore(login_operator, login_sadmin, get_baseurl, get_version, get_oracleclientip, get_oracleDatabaseName, cluster_idSet, get_oracle_user, jobinfo, expected):
    file = open('/eisoo/CZB-Test/workspace/6-0-Post_Upgrade_Validation/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    clientIP = get_oracleclientip
    databasename = get_oracleDatabaseName
    oracleuser = get_oracle_user
    
    url = parse.urljoin(base_url, res['restore_job_url'])
    referer = parse.urljoin(base_url, res['restore_job_referer'])
    method = res['restore_job_method']

    if clientIP == False:
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
    gnsPath, BackupType, timestamp = common.get_last_timepoint(login_operator, base_url, version, cluster_idSet, 'oracle')
    timepoint = common.timestamptopoint(login_operator, base_url, version, cluster_idSet, 'oracle')
    jobinfo['clusterId'] = clusterId
    jobinfo['clusterVip'] = vip
    jobinfo['jobClientId'] = clientId
    jobinfo['jobCreatorId'] =  userId
    jobinfo['jobDestClientId'] = clientId
    jobinfo['jobDatabaseRunUsername'] = oracleuser
    jobinfo['jobId'] = common.jobId_from_jobName(base_url, version, login_operator, 'oracle')
    jobinfo['jobRelatedId'] = common.jobId_from_jobName(base_url, version, login_operator, 'oracle')
    jobinfo['jobName'] = common.get_restore_jobname(login_operator, base_url, version, 'oracle')
    dispPath = '[' + '"' + "%s" %timepoint + '"' + "," + '"' + "%s" %databasename + '"' + ']'
    jobinfo['jobAdvParam'] = [{"key": "EEE_CUSTOM_SCRIPT", "value": "0"},
                              {"key": "EEE_LANFREE_OPEN_FC", "value": "0"},
                              {"key": "EEE_RESTORE_GNS", "value": "%s" %(gnsPath)},
                              {"key": "EEE_RESTORE_DATASOURCE", "value": "%s" %(databasename)},
                              {"key": "EEE_ORACLE_RESTORE_OBJECT_TYPE", "value": "0"},
                              {"key": "EEE_ORACLE_DATAFILE_COMMON_PATH", "value": ""},
                              {"key": "EEE_ORACLE_RESTORE_CTRLFILE_CHECKBOX", "value": "1"},
                              {"key": "EEE_ORACLE_RESTORE_ONLINE", "value": "1"},
                              {"key": "EEE_ORACLE_MUTIL_CHANNEL", "value": "0"},
                              {"key": "EEE_ORACLE_DATAFILE_MUTIL_CHANNEL_NUM", "value": "1"},
                              {"key": "EEE_ORACLE_ARCHFILE_MUTIL_CHANNEL_NUM", "value": "1"},
                              {"key": "EEE_ORACLE_BSET_COMMONPATH_DATAFILE", "value": "1"},
                              {"key": "EEE_ORACLE_BSET_DIFFPATH_DATAFILE", "value": "0"},
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

if __name__== '___main__':
    pytest.main(["test_02_oraclejob.py --Console_URL=base_url --Version=version --oracle_ClientIP=clientIP --oracle_ClientPwd=clientPwd --oracle_DatabaseName=databasename"])
