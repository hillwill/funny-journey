import sys
sys.path.append("D:\\workspace\\TaskRun-status")
import pytest
import requests
import xlwt
import yaml
from urllib import parse
from common import general
import xlrd
from xlutils.copy import copy
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

workbook = xlwt.Workbook()

def test_ScheduledResult_Write01(sh_login_operator, get_Time):
    """获取上海本部上线环境定时备份任务上周运行情况，并记录到表"""
    file = open('D:\\workspace\\TaskRun-status\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['sh_base_url'], res['backupResult_url'])
    cookie = sh_login_operator
    csrftoken = sh_login_operator['csrftoken']
    referer = res['sh_backupResult_headers']['Referer']
    header = {"referer": "%s" % (referer),
              "x-csrftoken": "%s" % (csrftoken)}

    # reason_url = parse.urljoin(res['sh_base_url'], res['backupReason_url'])
    # reason_header = res['sh_backupReason_headers']
    # reason_cookie = cookie
    s = general.GetHistory()
    jobType, jobTotal, jobTime = s.run_main('Scheduled', url, header, cookie, get_Time)

    sheet01 = workbook.add_sheet("上海总部")
    i = 0
    for i in range(len(jobTotal)):
        sheet01.write(i, 0, jobTime[i])
        sheet01.write(i, 1, '192.168.140.55')
        sheet01.write(i, 2, jobType[i])
        sheet01.write(i, 3, jobTotal[i])
        i = i+1

    workbook.save("D:\\workspace\\TaskRun-status\\TestResult\\ONLINE-Test.xls")

def test_ScheduledResult_Write02(shidc_login_operator, get_Time):
    """获取上海IDC上线环境定时备份任务上周运行情况，并记录到表"""
    file = open('D:\\workspace\\TaskRun-status\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['shidc_base_url'], res['backupResult_url'])
    cookie = shidc_login_operator
    csrftoken = shidc_login_operator['csrftoken']
    referer = res['shidc_backupResult_headers']['Referer']
    header = {"referer": "%s" % (referer),
              "x-csrftoken": "%s" % (csrftoken)}

    # reason_url = parse.urljoin(res['shidc_base_url'], res['backupReason_url'])
    # reason_header = res['shidc_backupReason_headers']
    # reason_cookie = cookie
    s = general.GetHistory()
    jobType, jobTotal, jobTime = s.run_main('Scheduled', url, header, cookie, get_Time)

    sheet02 = workbook.add_sheet("上海IDC")
    i = 0
    for i in range(len(jobTotal)):
        sheet02.write(i, 0, jobTime[i])
        sheet02.write(i, 1, '10.4.8.6')
        sheet02.write(i, 2, jobType[i])
        sheet02.write(i, 3, jobTotal[i])
        i = i + 1

    workbook.save("D:\\workspace\\TaskRun-status\\TestResult\\ONLINE-Test.xls")
#
# def test_ScheduledResult_Write03(wxidc_login_operator, get_Time):
#     """获取无锡IDC上线环境定时备份任务上周运行情况，并记录到表"""
#     file = open('D:\\workspace\\TaskRun-status\\TestData\\config.yaml', encoding='utf-8')
#     res = yaml.load(file, Loader=yaml.FullLoader)
#     url = parse.urljoin(res['wxidc_base_url'], res['backupResult_url'])
#     cookie = wxidc_login_operator
#     csrftoken = wxidc_login_operator['csrftoken']
#     referer = res['wxidc_backupResult_headers']['Referer']
#     header = {"referer": "%s" % (referer),
#               "x-csrftoken": "%s" % (csrftoken)}
#
#     # reason_url = parse.urljoin(res['wxidc_base_url'], res['backupReason_url'])
#     # reason_header = res['wxidc_backupReason_headers']
#     # reason_cookie = cookie
#     s = general.GetHistory()
#     jobType, jobTotal, jobTime = s.run_main('Scheduled', url, header, cookie, get_Time)
#
#     sheet03 = workbook.add_sheet("无锡IDC")
#     i = 0
#     for i in range(len(jobTotal)):
#         sheet03.write(i, 0, jobTime[i])
#         sheet03.write(i, 1, '10.10.1.229')
#         sheet03.write(i, 2, jobType[i])
#         sheet03.write(i, 3, jobTotal[i])
#         i = i + 1
#
#     workbook.save("D:\\workspace\\TaskRun-status\\TestResult\\ONLINE-Test.xls")

def test_CDMResult_Write01(sh_login_operator, get_Time):
    """获取上海总部上线环境副本备份任务上周运行情况，并记录到表"""
    file = open('D:\\workspace\\TaskRun-status\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['sh_base_url'], res['cdmResult_url'])
    cookie = sh_login_operator
    csrftoken = sh_login_operator['csrftoken']
    referer = res['sh_cdmResult_headers']['Referer']
    header = {"referer": "%s" % (referer),
              "x-csrftoken": "%s" % (csrftoken)}

    # reason_url = parse.urljoin(res['sh_base_url'], res['cdmReason_url'])
    # reason_header = res['sh_cdmReason_headers']
    # reason_cookie = cookie
    s = general.GetHistory()
    jobTotal, jobTime, jobType = s.run_main('CDM', url, header, cookie, get_Time)

    workbook = xlrd.open_workbook("D:\\workspace\\TaskRun-status\\TestResult\\ONLINE-Test.xls")
    all_sheet = workbook.sheet_names()
    old_sheet = workbook.sheet_by_name(all_sheet[0])
    old_rows = old_sheet.nrows
    new_workbook = copy(workbook)
    new_sheet01 = new_workbook.get_sheet(0)
    i = 0
    for i in range(len(jobTotal)):
        new_sheet01.write(old_rows+i, 0, jobTime[i])
        new_sheet01.write(old_rows+i, 1, '192.168.140.55')
        new_sheet01.write(old_rows+i, 2, jobType[i])
        new_sheet01.write(old_rows+i, 3, jobTotal[i])
        i = i + 1

    new_workbook.save("D:\\workspace\\TaskRun-status\\TestResult\\ONLINE-Test.xls")

def test_CDMResult_Write02(shidc_login_operator, get_Time):
    """获取上海IDC上线环境副本备份任务上周运行情况，并记录到表"""
    file = open('D:\\workspace\\TaskRun-status\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['shidc_base_url'], res['cdmResult_url'])
    cookie = shidc_login_operator
    csrftoken = shidc_login_operator['csrftoken']
    referer = res['shidc_cdmResult_headers']['Referer']
    header = {"referer": "%s" % (referer),
              "x-csrftoken": "%s" % (csrftoken)}

    # reason_url = parse.urljoin(res['shidc_base_url'], res['cdmReason_url'])
    # reason_header = res['shidc_cdmReason_headers']
    # reason_cookie = cookie
    s = general.GetHistory()
    jobTotal, jobTime, jobType = s.run_main('CDM', url, header, cookie, get_Time)

    workbook = xlrd.open_workbook("D:\\workspace\\TaskRun-status\\TestResult\\ONLINE-Test.xls")
    all_sheet = workbook.sheet_names()
    old_sheet = workbook.sheet_by_name(all_sheet[1])
    old_rows = old_sheet.nrows
    new_workbook = copy(workbook)
    new_sheet02 = new_workbook.get_sheet(1)
    i = 0
    for i in range(len(jobTotal)):
        new_sheet02.write(old_rows + i, 0, jobTime[i])
        new_sheet02.write(old_rows + i, 1, '10.4.8.6')
        new_sheet02.write(old_rows + i, 2, jobType[i])
        new_sheet02.write(old_rows + i, 3, jobTotal[i])
        i = i + 1

    new_workbook.save("D:\\workspace\\TaskRun-status\\TestResult\\ONLINE-Test.xls")
#
# def test_CDMResult_Write03(wxidc_login_operator, get_Time):
#     """获取无锡IDC上线环境副本备份任务上周运行情况，并记录到表"""
#     file = open('D:\\workspace\\TaskRun-status\\TestData\\config.yaml', encoding='utf-8')
#     res = yaml.load(file, Loader=yaml.FullLoader)
#     url = parse.urljoin(res['wxidc_base_url'], res['cdmResult_url'])
#     cookie = wxidc_login_operator
#     csrftoken = wxidc_login_operator['csrftoken']
#     referer = res['wxidc_cdmResult_headers']['Referer']
#     header = {"referer": "%s" % (referer),
#               "x-csrftoken": "%s" % (csrftoken)}
#
#     # reason_url = parse.urljoin(res['wxidc_base_url'], res['cdmReason_url'])
#     # reason_header = res['wxidc_cdmReason_headers']
#     # reason_cookie = cookie
#     s = general.GetHistory()
#     jobTotal, jobTime, jobType = s.run_main('CDM', url, header, cookie, get_Time)
#
#     workbook = xlrd.open_workbook("D:\\workspace\\TaskRun-status\\TestResult\ONLINE-Test.xls")
#     all_sheet = workbook.sheet_names()
#     old_sheet = workbook.sheet_by_name(all_sheet[2])
#     old_rows = old_sheet.nrows
#     new_workbook = copy(workbook)
#     new_sheet03 = new_workbook.get_sheet(2)
#     i = 0
#     for i in range(len(jobTotal)):
#         new_sheet03.write(old_rows + i, 0, jobTime[i])
#         new_sheet03.write(old_rows + i, 1, '10.10.1.229')
#         new_sheet03.write(old_rows + i, 2, jobType[i])
#         new_sheet03.write(old_rows + i, 3, jobTotal[i])
#         i = i + 1

def test_SelfResult_Write01(sh_login_admin, get_Time):
    """获取上海总部上线环境自备份任务上周运行情况，并记录到表格"""
    file = open('D:\\workspace\\TaskRun-status\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['sh_base_url'], res['selfResult_url'])
    cookie = sh_login_admin
    csrftoken = sh_login_admin['csrftoken']
    referer = res['sh_selfResult_headers']['Referer']
    header = {"referer": "%s" % (referer),
              "x-csrftoken": "%s" % (csrftoken)}

    s = general.GetHistory()
    jobTime = s.run_main('self', url, header, cookie, get_Time)

    workbook = xlrd.open_workbook("D:\\workspace\\TaskRun-status\\TestResult\\ONLINE-Test.xls")
    all_sheet = workbook.sheet_names()
    old_sheet = workbook.sheet_by_name(all_sheet[0])
    old_rows = old_sheet.nrows
    new_workbook = copy(workbook)
    new_sheet04 = new_workbook.get_sheet(0)
    i = 0
    for i in range(len(jobTime)):
        new_sheet04.write(old_rows + i, 0, jobTime[i])
        new_sheet04.write(old_rows + i, 1, '192.168.140.55')
        new_sheet04.write(old_rows + i, 2, '自备份')
        new_sheet04.write(old_rows + i, 3, '自备份失败')
        i = i + 1

    new_workbook.save("D:\\workspace\\TaskRun-status\\TestResult\\ONLINE-Test.xls")

def test_SelfResult_Write02(shidc_login_admin, get_Time):
    """获取上海总部上线环境副本备份任务上周运行情况，并记录到表"""
    file = open('D:\\workspace\\TaskRun-status\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    url = parse.urljoin(res['shidc_base_url'], res['selfResult_url'])
    print(url)
    cookie = shidc_login_admin
    csrftoken = shidc_login_admin['csrftoken']
    referer = res['shidc_selfResult_headers']['Referer']
    header = {"referer": "%s" % (referer),
              "x-csrftoken": "%s" % (csrftoken)}

    s = general.GetHistory()
    jobTime = s.run_main('self', url, header, cookie, get_Time)

    workbook = xlrd.open_workbook("D:\\workspace\\TaskRun-status\\TestResult\\ONLINE-Test.xls")
    all_sheet = workbook.sheet_names()
    old_sheet = workbook.sheet_by_name(all_sheet[1])
    old_rows = old_sheet.nrows
    new_workbook = copy(workbook)
    new_sheet04 = new_workbook.get_sheet(0)
    new_sheet05 = new_workbook.get_sheet(1)
    i = 0
    for i in range(len(jobTime)):
        new_sheet05.write(old_rows + i, 0, jobTime[i])
        new_sheet05.write(old_rows + i, 1, '10.4.8.6')
        new_sheet05.write(old_rows + i, 2, '自备份')
        new_sheet05.write(old_rows + i, 3, '自备份失败')
        i = i + 1

    new_workbook.save("D:\\workspace\\TaskRun-status\\TestResult\\ONLINE-Test.xls")

    new_sheet04.col(0).width = 256 * 20
    new_sheet04.col(1).width = 256 * 20
    new_sheet04.col(2).width = 256 * 20
    new_sheet04.col(3).width = 256 * 35

    new_sheet05.col(0).width = 256 * 20
    new_sheet05.col(1).width = 256 * 15
    new_sheet05.col(2).width = 256 * 30
    new_sheet05.col(3).width = 256 * 35

    new_workbook.save("D:\\workspace\\TaskRun-status\\TestResult\\ONLINE-Test.xls")
#
# def test_SelfResult_Write03(wxidc_login_admin, get_Time):
#     """获取上海总部上线环境副本备份任务上周运行情况，并记录到表"""
#     file = open('D:\\workspace\\TaskRun-status\\TestData\\config.yaml', encoding='utf-8')
#     res = yaml.load(file, Loader=yaml.FullLoader)
#     url = parse.urljoin(res['wxidc_base_url'], res['selfResult_url'])
#     cookie = wxidc_login_admin
#     csrftoken = wxidc_login_admin['csrftoken']
#     referer = res['wxidc_selfResult_headers']['Referer']
#     header = {"referer": "%s" % (referer),
#               "x-csrftoken": "%s" % (csrftoken)}
#
#     s = general.GetHistory()
#     jobTime = s.run_main('self', url, header, cookie, get_Time)
#
#     workbook = xlrd.open_workbook("D:\\workspace\\TaskRun-status\\TestResult\\ONLINE-Test.xls")
#     all_sheet = workbook.sheet_names()
#     old_sheet = workbook.sheet_by_name(all_sheet[2])
#     old_rows = old_sheet.nrows
#     new_workbook = copy(workbook)
#     new_sheet04 = new_workbook.get_sheet(0)
#     new_sheet05 = new_workbook.get_sheet(1)
#     new_sheet06 = new_workbook.get_sheet(2)
#     i = 0
#     for i in range(len(jobTime)):
#         new_sheet06.write(old_rows + i, 0, jobTime[i])
#         new_sheet06.write(old_rows + i, 1, '10.10.1.229')
#         new_sheet06.write(old_rows + i, 2, '自备份')
#         new_sheet06.write(old_rows + i, 3, '自备份失败')
#         i = i + 1
#
#     new_workbook.save("D:\\workspace\\TaskRun-status\\TestResult\\ONLINE-Test.xls")
#
#     new_sheet04.col(0).width = 256 * 20
#     new_sheet04.col(1).width = 256 * 20
#     new_sheet04.col(2).width = 256 * 20
#     new_sheet04.col(3).width = 256 * 35
#
#     new_sheet05.col(0).width = 256 * 20
#     new_sheet05.col(1).width = 256 * 15
#     new_sheet05.col(2).width = 256 * 30
#     new_sheet05.col(3).width = 256 * 35
#
#     new_sheet06.col(0).width = 256 * 20
#     new_sheet06.col(1).width = 256 * 18
#     new_sheet06.col(2).width = 256 * 28
#     new_sheet06.col(3).width = 256 * 30
#
#     new_workbook.save("D:\\workspace\\TaskRun-status\\TestResult\\ONLINE-Test.xls")

if __name__ == "__main__":
    pytest.main(["test_Restult_Write.py"])