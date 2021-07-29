#!/bin/bash

echo $1
#解压及安装
cd $1
tar -zxf ServerPackage -C $1
cd AnyBackupServer/
pwd
install
