#!/usr/bin/env python3
#*-*coding:utf-8*-*
import sys,re
import os
import subprocess
import argparse
import paramiko

# scp file to remote node.
def Connect_RemoteNode(user,ip,password,localsource,remotedest,port):
    SCP_CMD_BASE = r"""
        expect -c "
        set timeout 300 ;
        spawn scp -P {port} {localsource} {username}@{host}:{remotedest} ;
        expect {{{{
            *yes/no* {{{{ send "yes"\r }}}}
            *assword* {{{{ send {password}\r }}}}
        }}}}
        expect *\r ;
        expect \r ;
        expect eof
        "
    """.format(username=user,password=password,host=ip,localsource=localsource,remotedest=remotedest,port=port)
    SCP_CMD = SCP_CMD_BASE.format(localsource = localsource)
    print("execute SCP_CMD: ",SCP_CMD)
    p = subprocess.Popen( SCP_CMD , stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p.communicate()
    os.system(SCP_CMD)

# do updatesoft in remote node.
def Update_ClientSoft(ip, port, password):
    print(ip)
    print(port) 
    print(password)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=ip,
                    port=port,
                    username='root',
                    password=password,
                    timeout=60)
        print('客户端连接成功!')
    except Exception as e:
        print('客户端连接错误!', e)

    try:        
        stdin, stdout, stderr = ssh.exec_command('cd /opt; chmod +x Uchange.sh; ./Uchange.sh; ./Udeploy.sh')
        print(stdout.read().decode('utf-8'))
        print('客户端升级成功:%s'%ip)
    except Exception as e:
        print('客户端升级错误:%s' %ip, e)
    
def Do_Connect_andInstall():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ClientPackageNew', default='')
    parser.add_argument('--Client_IP', default='')
    parser.add_argument('--Client_Pwd', default='')
    args = parser.parse_args()

    ip = args.Client_IP
    password = args.Client_Pwd
    if password == 'Driver!@#$5678':
        tpassword = r'Driver!@#\\\$5678'
    if password == 'eisoo.com123':
        tpassword = r'eisoo.com123'
    local_file = "ClientPackageNew Uchange.sh Udeploy.sh"
    Connect_RemoteNode("root", ip, tpassword, local_file, "/opt", 22)
    Update_ClientSoft(ip, 22, password)
        
Do_Connect_andInstall()
