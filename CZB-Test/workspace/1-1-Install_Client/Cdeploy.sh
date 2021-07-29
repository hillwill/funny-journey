#!/bin/bash

#解压及安装
tar -zmxf /opt/ClientPackage -C /opt/
cd /opt/AnyBackupClient/ClientService/
install
