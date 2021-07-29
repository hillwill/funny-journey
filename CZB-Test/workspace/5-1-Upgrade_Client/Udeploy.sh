#!/bin/bash

mv /opt/AnyBackupClient/ /opt/AnyBackupClient-bak/
tar -zmxf /opt/ClientPackageNew -C /opt/
cd /opt/AnyBackupClient/ClientService/
install
