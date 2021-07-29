#!/usr/bin/env python3
#*-*coding:utf-8*-*
import sys,re
import os
import subprocess
import argparse
import paramiko
import pytest
import allure

@allure.title("卸载低版本客户端成功！")
def test_un_client(get_clientip, get_clientusername, get_clientpwd):
    """卸载旧版本客户端"""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=get_clientip,
                    port=22,
                    username='root',
                    password=get_clientpwd,
                    timeout=60)
        print('客户端连接成功!')
    except Exception as e:
        print('客户端连接错误!', e)

    try:
        stdin, stdout, stderr = ssh.exec_command('cd /opt/AnyBackupClient/ClientService/; echo "yes" | ./uninstall.sh; rm -rf /opt/AnyBackupClient/')
        print(stdout.read().decode('utf-8'))
        print('客户端卸载成功!')
    except Exception as e:
        print('客户端卸载错误!', e)

if __name__== '___main__':
    pytest.main(["test_01_un.py --Client_IP=clientip --Client_Username=clientusername --Client_Pwd=clientpwd"])
