#!/bin/bash

cd /opt/AnyBackupClient/ClientService/
echo "yes" | ./uninstall.sh
file1=/opt/Udeploy.sh
file2=/opt/install.cfg
coco=`cat $file2`
sed -i "s:install:$coco:g" $file1
