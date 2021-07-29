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

@allure.title("分配oracle任务的客户端成功！")
@pytest.mark.parametrize("clientinfo, expected",
                         [
                             ({"clientIsBuildin": "false",
                               "nodeIp": "",
                               "requestId": "",
                               "userNames": ["test"]}, "success"),
                         ])
def test_client(login_sadmin, get_baseurl, get_version, get_oracleclientip, clientinfo, expected):
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

    clientId, clientName = common.client_details_from_IP(base_url, version, login_sadmin, get_oracleclientip)
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

@allure.title("oracle授权成功！")
@pytest.mark.parametrize("datainfo, expected",
                         [
                             ({"customer": "using_sqlAuth",
                               "engineType": 4001,
                               "isManual": "false",
                               "isTest": "false",
                               "jobType": "eso_backupengine_oracleengine",
                               "port": 1433}, "success"),
                         ])
def test_database_verify(get_baseurl, get_version, login_operator, login_sadmin, get_oracle_user, get_oracleDatabaseName, get_oracleAuthUserName, get_oracleAuthPassword, get_oracleclientip, get_groupId, datainfo, expected):
    file = open('/eisoo/CZB-Test/workspace/4-0-Prepare_Job/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    clientId, clientName = common.client_details_from_IP(base_url, version, login_sadmin, get_oracleclientip)

    url = parse.urljoin(base_url, res['verify_database_url']).format(clientId)
    referer = parse.urljoin(base_url, res['verify_database_referer'])
    method = res['verify_database_method']
    if version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_operator
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    datainfo['osUserName'] = get_oracle_user
    datainfo['dbName'] = get_oracleDatabaseName
    datainfo['instanceName'] = get_oracleDatabaseName
    datainfo['username'] = get_oracleAuthUserName
    datainfo['password'] = get_oracleAuthPassword

    print(f'url:{url}')
    print(f'header:{header}')
    print(f'datainfo:{datainfo}')

    s = common.Webrequests()
    response = s.run_main(method, url, datainfo, header, cookie)
    print(response)

@allure.title("创建Oracle定时备份任务成功！")
@pytest.mark.parametrize("jobinfo, expected",
                         [
                             ({"jobDesc": "",
                               "jobName": "oracle",
                               "jobDatabaseRunUsername": "oracle",
                               "jobPlanId": "",
                               "jobStorageId": "1",
                               "jobType": "eso_backupengine_oracleengine"}, "success"),
                         ])
def test_Createjob(login_operator, login_sadmin, get_baseurl, get_version, get_oracleclientip, get_oracleDatabaseName, get_oracle_customer, get_groupId, jobinfo, expected):
    file = open('/eisoo/CZB-Test/workspace/4-0-Prepare_Job/TestData/config.yaml')
    res = yaml.load(file, Loader=yaml.FullLoader)
    base_url = get_baseurl
    version = get_version
    datasource = get_oracleDatabaseName
    clientIP = get_oracleclientip
    customer = get_oracle_customer
    clientId, clientName = common.client_details_from_IP(base_url, version, login_sadmin, get_oracleclientip)

    url = parse.urljoin(base_url, res['job_url'])
    referer = parse.urljoin(base_url, res['job_referer'])
    method = res['job_method']

    if clientIP == False:
        pytest.skip(msg='This test if only for oracle backup')
    elif version in ('7.0.8.0', '7.0.9.1', '7.0.10.0', '7.0.11.0'):
        cookie, userId = login_operator
        header = {"referer": "%s" % (referer)}
    else:
        cookie, userId, csrftoken = login_operator
        header = {"referer": "%s" % (referer),
                  "x-csrftoken": "%s" % (csrftoken)}
    
    jobinfo['jobCreatorId'] = userId
    jobinfo['jobClientId'] = clientId
    dispath = '[' + '"%s(%s)"' %(clientName, clientIP) + "," + '"Oracle数据库备份服务器"' + "," + '"%s"' %datasource + ']'
    jobinfo['jobDataSource'] = [{"fullPath": "%s" %datasource,
                                 "dispPath": "%s" %dispath,
                                 "customer": "%s" %customer,
                                 "nodeType": 2001,
                                 "uuid": ""}]
    jobinfo['jobAdvParam'] = [{"key": "EEE_ORACLE_BSET_BACKUP_ARCHDAYS", "value": "0"},
                              {"key": "EEE_ORACLE_ARCHIVE_BACKUPDAYS", "value": "3"},
                              {"key": "EEE_UNIT_OF_TIME_FOR_BACKUP_ARCH", "value": "4"},
                              {"key": "EEE_IS_DELETE_ARCHIVE_LOG", "value": "0"},
                              {"key": "EEE_DELETE_ARCHIVE_LOG_TIME", "value": "3"},
                              {"key": "EEE_UNIT_OF_TIME_FOR_DELETE_ARCH", "value": "4"},
                              {"key": "EEE_LANFREE_OPEN_FC", "value": "0"},
                              {"key": "EEE_FLOW_CONTROL_ENABLE", "value": "0"},
                              {"key": "EEE_ORACLE_MUTIL_CHANNEL", "value": "0"},
                              {"key": "EEE_ORACLE_DATAFILE_MUTIL_CHANNEL_NUM", "value": "1"},
                              {"key": "EEE_ORACLE_ARCHFILE_MUTIL_CHANNEL_NUM", "value": "1"},
                              {"key": "EEE_ORACLE_BSET_FILESPERSET", "value": "0"},
                              {"key": "EEE_ORACLE_FILESPERSET_DATAFILE_NUMBER", "value": "32"},
                              {"key": "EEE_ORACLE_FILESPERSET_ARCHIVE_NUMBER", "value": "32"},
                              {"key": "EEE_ORACLE_BCT_IS_OPEN", "value": "0"},
                              {"key": "EEE_ORACLE_BSET_BLKSIZE", "value": "0"},
                              {"key": "EEE_ORACLE_BLKSIZE_NUMBER", "value": "0.25"},
                              {"key": "EEE_ORACLE_BSET_MAXOPENFILES", "value": "0"},
                              {"key": "EEE_ORACLE_MAXOPENFILES_NUMBER", "value": "8"},
                              {"key": "EEE_ORACLE_BSET_MAXPIECESIZE", "value": "1"},
                              {"key": "EEE_ORACLE_MAXPIECESIZE_NUMBER", "value": "30"},
                              {"key": "EEE_ORACLE_USE_SECTION_SIZE", "value": "0"},
                              {"key": "EEE_ORACLE_SECTION_SIZE", "value": "30"},
                              {"key": "EEE_ORACLE_SECTION_SIZE_UNIT", "value": "1"},
                              {"key": "EEE_ORACLE_USE_SKIPCORRUPT_DATAFILE", "value": "0"},
                              {"key": "EEE_ORACLE_BACKUP_PFILE", "value": "1"},
                              {"key": "EEE_ORACLE_BACKUP_COMPRESS", "value": "0"},
                              {"key": "EEE_ORACLE_SKIP_READONLY_TBSPACE", "value": "0"},
                              {"key": "EEE_ORACLE_SKIP_OFFLINE_DATA", "value": "0"},
                              {"key": "EEE_ENCRYPTION_XXXX", "value": "0"},
                              {"key": "EEE_DEDUP", "value": "0"},
                              {"key": "EEE_CUSTOM_SCRIPT", "value": "0"},
                              {"key": "EEE_COMPRESS_ALGO_CHECKED", "value": "0"},
                              {"key": "EEE_DELETE_ARCHIVE_LOG_ALL", "value": "0"},
                              {"key": "EEE_AUTO_RESTART", "value": "0"},
                              {"key": "EEE_AUTO_RESTART_COUNT", "value": "1"},
                              {"key": "EEE_AUTO_RESTART_INTERVAL", "value": "1"},
                              {"key": "EEE_JOB_RUN_IMMEDIATELY", "value": "1"}]
    
    print(jobinfo)
    print(header)
    print(cookie)
    s = common.Webrequests()
    response = s.run_main(method, url, jobinfo, header, cookie)
    print(response)
    assert response['status'] == expected

@allure.title("发起Oracle定时备份任务成功！")
@pytest.mark.parametrize("jobinfo, expected",
                         [
                             ({"jobBackupType": 1,
                               "jobDesc": "",
                               "jobStatus": 4}, "success"),
                         ])
def test_Runjob(login_operator, get_baseurl, get_version, get_oracleclientip, jobinfo, expected):
    file = open('/eisoo/CZB-Test/workspace/4-0-Prepare_Job/TestData/config.yaml')
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

if __name__== '___main__':
    pytest.main(["test_04_oracle.py --Console_URL=base_url --Version=version --oracle_ClientIP=oracleclientip --oracle_DatabaseName=dbname --oracle_AuthUserName=username --oracle_AuthPassword=password"])
