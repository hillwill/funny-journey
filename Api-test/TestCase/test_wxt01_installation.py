import sys
sys.path.append("D:\\MyProject\\Api-test")
import paramiko
import pytest
import allure
import yaml

@allure.title('控制台安装成功!')
def test_console_installation():
    file = open('D:\\MyProject\\Api-test\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    hostname = res['hostname']
    username = res['username']
    password = res['password']
    port = res['port']
    #连接控制台
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=hostname,
                    port=port,
                    username=username,
                    password=password,
                    timeout=60)
    except Exception as e:
        print('控制台连接错误!', e)
    try:
        #上传和解压控制台包
        stdin, stdout, stderr = ssh.exec_command('cd /eisoo/;wget ftp://ftp-ab.aishu.cn/FTP/ci-jobs/AB7.0.10/package/AnyBackupServer/Linux_el7_x64/Linux_el7_x64-latest.tar.gz;tar -zxf Linux_el7_x64-latest.tar.gz')
        print(stdout.read())
    except Exception as e:
        print('控制台上传和解压包错误!',e)
    try:
        #安装控制台
        stdin, stdout, stderr = ssh.exec_command('cd /eisoo/AnyBackupServer;./install.sh --product=CDM --server-type=MASTER --self-ip=10.2.12.75 --cluster-id=25 --cluster-vip=10.2.12.76 --install-db=yes --db-id=26 --db-vip=10.2.12.77 --ssl=no')
        print(stdout.read())
        ssh.close()
    except Exception as e:
        print('控制台安装失败!',e)

@allure.title('客户端安装成功!')
def test_client_installation():
    file = open('D:\\MyProject\\Api-test\\TestData\\config.yaml', encoding='utf-8')
    res = yaml.load(file, Loader=yaml.FullLoader)
    hostname = res['clienthostname']
    username = res['clientusername']
    password = res['clientpassword']
    port = res['clientport']
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=hostname,
                    port=port,
                    username=username,
                    password=password,
                    timeout=60)
    except Exception as e:
        print('客户端连接错误!', e)
    try:
        #上传和解压客户端包
        stdin, stdout, stderr = ssh.exec_command('cd /eisoo/;wget ftp://ftp-ab.aishu.cn/FTP/ci-jobs/AB7.0.10/package/AnyBackupClient/Linux_el7_x64/Linux_el7_x64-latest.tar.gz;tar -zmxf Linux_el7_x64-latest.tar.gz')
        print(stdout.read())
    except Exception as e:
        print('客户端上传和解压包错误!',e)
    try:
        #安装客户端
        stdin, stdout, stderr = ssh.exec_command('cd /eisoo/AnyBackupClient/ClientService;./install.sh 10.2.12.87 10.2.12.76 Chinese no_volume_cdp force n')
        print(stdout.read())
        ssh.close()
    except Exception as e:
        print('安装失败!',e)

if __name__ == "__main__":
    pytest.main(["test_01_installation.py"])