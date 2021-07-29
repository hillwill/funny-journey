#!/bin/bash

file1=/opt/Cdeploy.sh
file2=/opt/install.cfg
coco=`cat $file2`
sed -i "s:install:$coco:g" $file1
