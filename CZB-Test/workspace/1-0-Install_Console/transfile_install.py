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

# do install and patch in remote node.
def Install_Server(ip, port, password, installpath):
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
        stdin, stdout, stderr = ssh.exec_command('sh /%s/Schange.sh %s' %(installpath, installpath))
        stdin, stdout, stderr = ssh.exec_command('sh /%s/Sdeploy.sh %s' %(installpath, installpath))
        print(stdout.read().decode('utf-8'))
        print('部署成功:%s'%ip)
    except Exception as e:
        print('部署错误:%s' %ip, e)

#    try:
#        stdin, stdout, stderr = ssh.exec_command('rm -f /%s/Schange.sh  /%s/Sdeploy.sh' %(installpath, installpath))
#        print(stdout.read().decode('utf-8'))
#        print('清理成功:%s'%ip)
#    except Exception as e:
#        print('清理错误:%s' %ip, e)

def Do_Connect_andInstall():
    # get web parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('--ServerPackage', default='')
    parser.add_argument('--Install_Path', default='')
    parser.add_argument('--Console_IP', default='')
    parser.add_argument('--Console_Username', default='')
    parser.add_argument('--Console_Pwd', default='')
    parser.add_argument('--Console_Port', default='')
    args = parser.parse_args()

    # wget Console Package
    PackagePath = args.ServerPackage
    Rename = 'ServerPackage'
    wget.download(PackagePath, Rename)

    # connect nodes and install
    ip_list = args.Console_IP.split(',')
    for ip in ip_list:
        print(ip_list)
        print(ip)
        password = args.Console_Pwd
        if password == 'Driver!@#$5678':
            tpassword = r'Driver!@#\\\$5678'
        else:
            tpassword = r'%s' %(password)
        port = args.Console_Port
        installpath = args.Install_Path
        local_file = "Schange.sh Sdeploy.sh ServerPackage"
        Connect_RemoteNode("root", ip, tpassword, local_file, installpath, port)
        Install_Server(ip,  port, password, installpath)

# def Do_trans_patch_install():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--JiLin_Env_selfip', default='')
#     parser.add_argument('--NingXia_Env_selfip', default='')
#     parser.add_argument('--XIAN_Env_selfip', default='')
#     parser.add_argument('--XiaMen_Env_selfip', default='')
#     parser.add_argument('--ChongQing_Env_selfip', default='')
#     args = parser.parse_args()
#     env_list = ["JiLin","NingXia","XIAN","XiaMen","ChongQing"]
#     env_ip_list = [args.JiLin_Env_selfip, args.NingXia_Env_selfip, args.XIAN_Env_selfip, args.XiaMen_Env_selfip, args.ChongQing_Env_selfip]
#     env_order = 0
#     while env_order <= 4:
#         IP = env_ip_list[env_order]
#         if IP:
#             ip_list = IP.split(',')
#             for self_ip in ip_list:
#                 passwd = r"Driver!@#\\\$5678"
#                 local_file = "/eisoo/CZB-Test/workspace/Deploy_Env/label/10.2.12.102/%s" %env_list[env_order]
#                 scpFileToRemoteNode("root", self_ip, passwd, local_file, "/backupsoft", 5557)
#                 patch_install(self_ip,env_list,env_order)
#         env_order +=1


Do_Connect_andInstall()
