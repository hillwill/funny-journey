#!/usr/bin/env python3
#*-*coding:utf-8*-*
import sys,re
import os
import subprocess
import argparse
import paramiko
import wget

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
def Update_ServerSoft(ip, port, password, upgradepath):
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
        print('控制台连接成功!')
    except Exception as e:
        print('控制台连接错误!', e)

    try:        
        stdin, stdout, stderr = ssh.exec_command('sh /%s/Urun.sh %s' %(upgradepath, upgradepath))
        print(stdout.read().decode('utf-8'))
        print('升级执行结束:%s'%ip)
    except Exception as e:
        print('升级执行错误:%s' %ip, e)

    try:
        stdin, stdout, stderr = ssh.exec_command('rm -f /%s/input.data /%s/Urun.sh' %(upgradepath, upgradepath))
        print(stdout.read().decode('utf-8'))
        print('清理成功:%s'%ip)
    except Exception as e:
        print('清理错误:%s' %ip, e)

def Do_Connect_andUpdate():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ServerPackageNew', default='')
    parser.add_argument('--UpdatePackage', default='')
    parser.add_argument('--upgrade.json', default='')
    parser.add_argument('--Upgrade_Path', default='')
    parser.add_argument('--Console_IP', default='')
    parser.add_argument('--Console_Pwd', default='')
    parser.add_argument('--Console_Port', default='')
    args = parser.parse_args()
    
    # wget New Console Package
    PackagePath = args.ServerPackageNew
    Rename = 'ServerPackageNew'
    wget.download(PackagePath, Rename)
    
    # wget Update Package
    UpdatePkgPath = args.UpdatePackage
    UpdateRename = 'UpdatePackage'
    wget.download(UpdatePkgPath, UpdateRename)
    
    ip = args.Console_IP
    password = args.Console_Pwd
    if password == 'Driver!@#$5678':
        tpassword = r'Driver!@#\\\$5678'
    if password == 'eisoo.com123':
        tpassword = r'eisoo.com123'
    port = args.Console_Port
    upgradepath = args.Upgrade_Path
    local_file = "ServerPackageNew upgrade.json UpdatePackage input.data Urun.sh"
    Connect_RemoteNode("root", ip, tpassword, local_file, upgradepath, port)
    Update_ServerSoft(ip, port, password, upgradepath)
        
Do_Connect_andUpdate()
