#!/bin/bash

file1=$1/Sdeploy.sh
file2=$1/install.cfg
coco=`cat $file2`
sed -i "s:install:$coco:g" $file1
