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
    print "execute SCP_CMD: ",SCP_CMD
    p = subprocess.Popen( SCP_CMD , stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p.communicate()
    os.system(SCP_CMD)

# do updateos in remote node.
def Update_ServerOS(ip, port, password):
    print ip
    print port 
    print password
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
        stdin, stdout, stderr = ssh.exec_command('cd /opt/; mount ApolloPackage /mnt/cdrom; echo "y" | bash update_os.sh')
        print(stdout.read().decode('utf-8'))
        print('控制台系统升级成功:%s'%ip)
    except Exception as e:
        print('控制台系统升级错误:%s' %ip, e)

def Do_Connect_andInstall():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ApolloPackage', default='')
    parser.add_argument('--update_os.sh', default='')
    parser.add_argument('--Console_IP', default='')
    parser.add_argument('--Console_Pwd', default='')
    parser.add_argument('--Console_Port', default='')
    args = parser.parse_args()

    ip_list = args.Console_IP.split(',')
    for ip in ip_list:
	password = args.Console_Pwd
	print password
	if password == 'Driver!@#$5678':
            tpassword = r'Driver!@#\\\$5678'
	if password == 'eisoo.com123':
	    tpassword = r'eisoo.com123'
        port = args.Console_Port
        local_file = "ApolloPackage update_os.sh"
        Connect_RemoteNode("root", ip, tpassword, local_file, "/opt", port)
        Update_ServerOS(ip, port, password)
        
Do_Connect_andInstall()
