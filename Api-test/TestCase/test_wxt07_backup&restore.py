import sys
sys.path.append("D:\\MyProject\\Api-test")
from urllib import parse
import allure
import pytest
import requests
import yaml
import time
from time import sleep
from common import common
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

@allure.title("创建任务成功!")
@pytest.mark.parametrize("taskinfo, expected",
                         [
                             ({"backupMedia": "",
                               "clusterVip": "",
                               "filterDatas": [{"filterType": 1, "filterMode": 1, "content": []},
                                               {"filterType": 2, "filterMode": 1, "content": []},
                                               {"filterType": 3, "filterMode": 1, "content": {"filterTypes": [], "other": []}},
                                               {"filterType": 4, "filterMode": 1, "content": {}}],
                                "jobType": "eso_backupengine_fileengine",
                                "jobStorageId": "1",
                                "jobPlanId": "",
                                "jobName": "file1",
                                "jobDesc": "",
                                "jobDatabaseRunUsername": "",
                                "jobDataSource": [{"fullPath": "/recovery",
                                                   "dispPath": ["localhost.localdomain(10.2.12.87)","文件系统备份服务器","/","recovery"],
                                                   "customer": 0,
                                                   "nodeType": 1001,
                                                   "uuid": ""}],
                                "jobAdvParam": [{"key": "EEE_LANFREE_OPEN_FC", "value": "0"},
                                                {"key": "EEE_LANFREE_CHANNEL_COUNT", "value": "1"},
                                                {"key": "EEE_AUTO_RESTART", "value": "0"},
                                                {"key": "EEE_PERMANENT_INCREMENT"},
                                                {"key": "EEE_ENCRYPTION_XXXX"},
                                                {"key": "EEE_DEDUP"},
                                                {"key": "EEE_FLOW_CONTROL_NEW"},
                                                {"key": "EEE_FLOW_CONTROL"},
                                                {"key": "EEE_CUSTOM_SCRIPT"},
                                                {"key": "EEE_AUTO_RESTART_COUNT", "value": "1"},
                                                {"key": "EEE_AUTO_RESTART_INTERVAL", "value": "1"},
                                                {"key": "EEE_COMPRESS_ALGO_CHECKED", "value": "0"},
                                                {"key": "EEE_BACKUP_CHANNEL_CONFS", "value": "0"},
                                                {"key": "EEE_TRAVERSAL_THREAD", "value": "20"},
                                                {"key": "EEE_READER_THREAD", "value": "1"},
                                                {"key": "EEE_JOB_RUN_IMMEDIATELY", "value": "0"}]}, "success"),
                         ])
def test_create_backup(login_oldoperator, client_idSet, oldoperator_idSet, taskinfo, expected):
    file = open('D:\\MyProject\\Api-test\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['backup_url'])
    method = res['backup_method']
    header = res['backup_headers']
    cookie = login_oldoperator
    taskinfo['jobClientId'] = client_idSet
    taskinfo['jobCreatorId'] = oldoperator_idSet
    s = common.Webrequests()
    response = s.run_main(method, url, taskinfo, header, cookie)
    print(f'response:{response}')
    assert response['status'] == expected
    sleep(5)

@allure.title("启动备份任务成功!")
@pytest.mark.parametrize("jobinfo, expected",
                         [
                             ({"jobBackupType": 1, "jobStatus": 4, "jobDesc" :""}, "success"),
                             ({"jobBackupType": 2, "jobStatus": 4, "jobDesc" :""}, "success"),
                         ])
def test_runbackup(login_oldoperator, job_idSet, jobinfo, expected):
    file = open('D:\\MyProject\\Api-test\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['startup_url']).format(job_idSet)
    print(f'url:{url}')
    method = res['startup_method']
    print(f'method:{method}')
    header = res['startup_headers']
    print(f'header:{header}')
    cookie = login_oldoperator
    s = common.Webrequests()
    response = s.run_main(method, url, jobinfo, header, cookie)
    print(f'response:{response}')
    assert response['status'] == expected
    sleep(35)

@allure.title("启动恢复任务成功!")
@pytest.mark.parametrize("jobinfo, expected",
                         [
                             ({"jobType": "eso_backupengine_fileengine",
                               "jobStorageId": "1",
                               "jobDestClientName": "localhost.localdomain",
                               "jobDesc": "",
                               "jobDataProduceType": 1,
                               "clusterVip": "10.2.12.76"}, "success"),
                         ])
def test_run_restore(login_oldoperator, jobinfo, expected, client_idSet, job_idSet, timepointfull_idSet, timepoint01_idSet, timestamptopoint, timepoint02_idSet, timepoint03_idSet, cluster_idSet, oldoperator_idSet, jobname_idSet):
    """读取配置文件中的参数"""
    file = open('D:\\MyProject\\Api-test\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['base_url'], res['restore_url'])
    print(f'utl:{url}')
    method = res['restore_method']
    print(f'method:{method}')
    header = res['restore_headers']
    print(f'header:{header}')
    cookie = login_oldoperator
    print(f'cookie:{cookie}')

    """通过方法获取各种id"""
    jobinfo['jobName'] = jobname_idSet
    jobinfo['clusterId'] = cluster_idSet
    jobinfo['jobClientId'] = client_idSet
    jobinfo['jobDestClientId'] = client_idSet
    jobinfo['jobDestClientIp'] = res['clienthostname']
    jobinfo['jobCreatorId'] = oldoperator_idSet
    jobinfo['jobId'] = job_idSet
    jobinfo['jobRelatedId'] = job_idSet

    """通过方法获取gnsPath"""
    gnsPath = timepoint01_idSet
    fullgnsPath = timepointfull_idSet
    jobinfo["jobAdvParam"] = [{"key": "EEE_CUSTOM_SCRIPT", "value": "0"},
                              {"key": "EEE_LANFREE_OPEN_FC", "value": "0"},
                              {"key": "EEE_LANFREE_CHANNEL_COUNT", "value": "1"},
                              {"key": "EEE_TIMEPOINT_USER_CHOOSE", "value": gnsPath},
                              {"key": "EEE_RESTORE_GNS", "value": fullgnsPath+'/recovery/boot.log-20190924'},
                              {"key": "EEE_IS_MOUNT_RESTORE", "value": "0"},
                              {"key": "EEE_IS_SINGLE_RESTORE", "value": "1"},
                              {"key": "EEE_RESTORE_REPLACE_STRATEGY", "value": "0"},
                              {"key": "EEE_DATA_WRITE_THREAD", "value": "8"},
                              {"key": "EEE_RESTORE_PATH", "value": ""},
                              {"key": "EEE_JOB_RUN_IMMEDIATELY", "value": "1"}]

    """将时间戳转换成备份时间点"""
    jobinfo['jobDataSource'] =  [{"dispPath": [timestamptopoint, "/", "recovery", "boot.log-20190924"],
                                  "customer": "boot.log-20190924",
                                  "fullPath": fullgnsPath+'/recovery/boot.log-20190924'}]

    print(f'jobinfo:{jobinfo}')
    s = common.Webrequests()
    response = s.run_main(method, url, jobinfo, header, cookie)
    print(f'response:{response}')
    assert response['status'] == expected
    sleep(5)