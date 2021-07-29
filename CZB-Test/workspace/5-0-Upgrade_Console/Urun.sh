#!/bin/bash

tar -zxf $1/UpdatePackage -C $1
cd $1/AnyBackupUpdate
./upgrade.sh upgrade --uptoolpkg $1/UpdatePackage --conf $1/upgrade.json --softpkg $1/ServerPackageNew < $1/input.data
