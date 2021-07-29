import requests
import yaml
import time

def Get_jobResquest(url, jobinfo, header, cookie):
    try:
        r = requests.get(url, params=jobinfo, headers=header, verify=False, cookies=cookie)
        json_r = r.json()
        return json_r
    except BaseException as e:
        print("请求失败", str(e))

def Get_jobResult(response, line):
    # 获取定时失败和部分成功任务名和结果
    jobName = response['responseData']['data'][line]['instJobName']
    if response['responseData']['data'][line]['instStatus'] == 128:
        jobResult = '"' + jobName + '"' + '备份部分成功'
    else:
        jobResult = '"' + jobName + '"' + '备份失败'
    return jobResult

def Get_cdmjobResult(cdm_response, line):
    # 获取CDM失败和部分成功任务名和结果
    jobName = cdm_response['responseData']['data'][line]['jobName']
    if cdm_response['responseData']['data'][line]['jobStatus'] == 128:
        jobResult = '"' + jobName + '"' + '备份部分成功'
    else:
        jobResult = '"' + jobName + '"' + '备份失败'
    return jobResult

def Get_jobType(response, line):
    # 获取定时任务类型
    file = open('D:\workspace\TaskRun-status\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)

    instJobType = response['responseData']['data'][line]['instJobType']
    return res[instJobType]

def Get_cdmjobType(response, line):
    # 获取CDM任务类型
    file = open('D:\workspace\TaskRun-status\TestData\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)

    jobType = response['responseData']['data'][line]['jobType']
    return res[jobType]

def Get_jobTime(response, line):
    # 获取定时任务时间
    instStartTimeStamp = response['responseData']['data'][line]['instEndTime']
    instStartTimeStamp_ten = instStartTimeStamp / 1000
    timeArray = time.localtime(instStartTimeStamp_ten)
    jobTime = time.strftime("%Y-%m-%d", timeArray)
    return jobTime

def Get_cdmjobTime(cdm_response, line):
    # 获取CDM任务时间
    instStartTimeStamp = cdm_response['responseData']['data'][line]['jobEndTime']
    instStartTimeStamp_ten = instStartTimeStamp / 1000
    timeArray = time.localtime(instStartTimeStamp_ten)
    CDMTime = time.strftime("%Y-%m-%d", timeArray)
    return CDMTime

def Get_selfjobTime(self_response, line):
    # 获取自备份任务时间
    selfTime = self_response['responseData']['data'][line]['timePoint']
    return selfTime

def Get_jobinstId(response, line):
    # 获取任务instId
    instId = response['responseData']['data'][line]['instId']
    return instId

def Get_cdminstId(response, line):
    # 获取cdm任务instId
    instId = response['responseData']['data'][line]['instanceId']
    return instId

class GetHistory():
    def Get_ScheduledHistory(self, url, header, cookie, get_Time):
        # 获取一周的时间范围
        SevenDaysAgoTime = get_Time

        jobType = []
        jobTime = []
        jobTotal = []
        # 获取结果为部分成功的任务
        jobinfo = {"count": 15,
                   "hasRunning": 0,
                   "index": 0,
                   "status": '64,128'}
        line = 0
        # 获取所有失败和部分成功任务信息
        # print(f'url:{url}')
        # print(f'jobinfo:{jobinfo}')
        # print(f'header:{header}')
        # print(f'cookie:{cookie}')
        response = Get_jobResquest(url, jobinfo, header, cookie)
        # print(f'response:{response}')
        totalNum = response['responseData']['totalNum']
        # print(f'totalNum:{totalNum}')

        while totalNum:
            # 如果没有失败部分成功任务，则结束
            if totalNum == 0:
                return jobType, jobTotal, jobTime
            elif totalNum >= 14:
                max = 14
            else:
                max = totalNum-1

            while line <= max:
                # 如果存在部分成功任务，且该任务在最近一周内，则开始统计
                if str(Get_jobTime(response, line)) > str(SevenDaysAgoTime):
                    # 获取任务名写入jobTotal
                    jobTotal.append(Get_jobResult(response, line))
                    # 获取任务类型写入jobType
                    jobType.append(Get_jobType(response, line))
                    # 获取任务开始时间写入jobTime
                    jobTime.append(Get_jobTime(response, line))
                    # 获取任务执行输出中的报错信息写入jobReason
                    # jobReason.append(detail.Get_PSjobLogInfo(response, PS_line, reason_url, reason_header, reason_cookie))
                    line = line + 1
                # 否则停止统计
                else:
                    return jobType, jobTotal, jobTime

            jobinfo['index'] += 15
            response = Get_jobResquest(url, jobinfo, header, cookie)
            # print(f'response:{response}')
            totalNum = response['responseData']['totalNum']
            # print(f'totalNum:{totalNum}')
            line = 0

        return jobType, jobTotal, jobTime

    def Get_CDMHistory(self, url, header, cookie, get_Time):
        # 获取一周的时间范围
        SevenDaysAgoTime = get_Time

        jobType = []
        jobTime = []
        jobTotal = []

        datainfo = {'count': 15,
                    'index': 0,
                    'status': '64,128'}

        # 获取所有失败和部分成功任务信息
        cdm_response = Get_jobResquest(url, datainfo, header, cookie)
        totalNum = cdm_response['responseData']['totalNum']

        while totalNum:
            # 如果没有失败部分成功任务，则结束
            if totalNum == 0:
                return jobTotal, jobTime, jobType
            elif totalNum >= 14:
                max = 14
            else:
                max = totalNum - 1

            # 否则开始统计
            line = 0
            while line <= max:
                # 如果存在部分成功任务，且该任务在最近一周内，则开始统计
                if str(Get_cdmjobTime(cdm_response, line)) > str(SevenDaysAgoTime):
                    # 获取任务名写入jobTotal
                    jobTotal.append(Get_cdmjobResult(cdm_response, line))
                    # 获取任务类型写入jobType
                    jobType.append(Get_cdmjobType(cdm_response, line))
                    # 获取任务开始时间写入jobTime
                    jobTime.append(Get_cdmjobTime(cdm_response, line))
                    # 获取任务执行输出中的报错信息写入jobReason
                    # jobReason.append(detail.Get_cdmFailedjobLogInfo(Failed_response, Failed_line, reason_url, reason_header, reason_cookie))
                    line += 1
                # 否则停止统计
                else:
                    return jobTotal, jobTime, jobType

            datainfo['index'] += 15
            cdm_response = Get_jobResquest(url, datainfo, header, cookie)
            totalNum = cdm_response['responseData']['totalNum']

        return jobTotal, jobTime, jobType

    def Get_CDPHistory(self, url, header, cookie, get_Time):
        """略"""

    def Get_selfHistory(self, url, header, cookie, get_Time):
        # 获取一周的时间范围
        SevenDaysAgoTime = get_Time

        jobTime = []
        datainfo = {'count': 15,
                    'index': 0}

        # 获取所有任务信息
        self_response = Get_jobResquest(url, datainfo, header, cookie)
        totalNum = self_response['responseData']['totalNum']
        max = totalNum - 1
        line = 0
        while line <= max:
            # 如果存在部分成功任务，且该任务在最近一周内，则开始统计
            if str(Get_selfjobTime(self_response, line)) > str(SevenDaysAgoTime):
                if self_response['responseData']['data'][line]['status'] == 64:
                    # 获取任务名写入jobTotal
                    jobTime.append(Get_selfjobTime(self_response, line))
                    line += 1
                else:
                    line += 1
            # 否则停止统计
            else:
                return jobTime
        return jobTime

    def Get_RemoteHistory(self, url, header, cookie, get_Time):
        """略"""

    def run_main(self, backupType, url, header, cookie, get_Time):
        result = None
        if backupType == 'Scheduled':
            result = self.Get_ScheduledHistory(url, header, cookie, get_Time)
        elif backupType == 'CDM':
            result = self.Get_CDMHistory(url, header, cookie, get_Time)
        elif backupType == 'CDP':
            result = self.Get_CDPHistory(url, header, cookie, get_Time)
        elif backupType == 'self':
            result = self.Get_selfHistory(url, header, cookie, get_Time)
        elif backupType == 'remote':
            result = self.Get_RemoteHistory(url, header, cookie, get_Time)
        else:
            print("backupType值错误！！！")
        return result