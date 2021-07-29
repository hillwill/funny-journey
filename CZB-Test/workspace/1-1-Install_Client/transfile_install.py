#!/usr/bin/env python3
#*-*coding:utf-8*-*
import sys,re
import os
import subprocess
import argparse
import paramiko

# scp file to remote node.
def Connect_RemoteNode(user,ip,password,localsource,remotedest):
    SCP_CMD_BASE = r"""
        expect -c "
        set timeout 300 ;
        spawn scp  {localsource} {username}@{host}:{remotedest} ;
        expect {{{{
            *yes/no* {{{{ send "yes"\r }}}}
            *assword* {{{{ send {password}\r }}}}
        }}}}
        expect *\r ;
        expect \r ;
        expect eof
        "
    """.format(username=user,password=password,host=ip,localsource=localsource,remotedest=remotedest)
    SCP_CMD = SCP_CMD_BASE.format(localsource = localsource)
    print("execute SCP_CMD: ",SCP_CMD)
    p = subprocess.Popen( SCP_CMD , stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p.communicate()
    os.system(SCP_CMD)

# do install and patch in remote client.
def Install_Client(ip, password):
    print(ip)
    print(password)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=ip,
                    port=22,
                    username='root',
                    password=password,
                    timeout=60)
        print('客户端连接成功!')
    except Exception as e:
        print('客户端连接错误!', e)

    try:
        stdin, stdout, stderr = ssh.exec_command('cd /opt/; chmod 755 ./{Cchange.sh, Cdeploy.sh}; ./Cchange.sh; ./Cdeploy.sh')
        print(stdout.read().decode('utf-8'))
        print('部署成功:%s'%ip)
    except Exception as e:
        print('部署错误:%s' %ip, e)

    try:
        stdin, stdout, stderr = ssh.exec_command('cd /opt/; rm -f Cchange.sh  Cdeploy.sh')
        print(stdout.read().decode('utf-8'))
        print('清理成功:%s'%ip)
    except Exception as e:
        print('清理错误:%s' %ip, e)

def Do_Connect_andInstall():
    # get web parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('--ClientPackage', default='')
    parser.add_argument('--Client_IP', default='')
    parser.add_argument('--Client_Username', default='')
    parser.add_argument('--Client_Pwd', default='')
    parser.add_argument('--Client_Port', default='')
    args = parser.parse_args()

    # wget Client Package
    PackagePath = args.ClientPackage
    Rename = 'ClientPackage'
    wget.download(PackagePath, Rename)

    # connect node and install
    ip = args.Client_IP
    password = args.Client_Pwd
    if password == 'Driver!@#$5678':
        tpassword = r'Driver!@#\\\$5678'
    elif password == 'eisoo.com123':
        tpassword = r'eisoo.com123'
    else:
        tpassword = r'%s' %password
    local_file = "Cchange.sh Cdeploy.sh ClientPackage"
    Connect_RemoteNode("root", ip, tpassword, local_file, "/opt")
    Install_Client(ip,  password)

Do_Connect_andInstall()
