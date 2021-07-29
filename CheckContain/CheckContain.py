# -*- coding: UTF-8 -*-
import os, re, xlwt

def get_Shell_Config(file_Path):
    all_Shell_Config = list()

    for root, dirs, files in os.walk(file_Path):
        for f in files:
            file = os.path.join(root, f)
            if '.bat' in file or '.sh' in file or '.config' in file or '.ini' in file or '.txt' in file:
                all_Shell_Config.append(file)
            else:
                continue

    return all_Shell_Config


def Is_Chinese_Contain(package_Path):
    all_Shell_Config = get_Shell_Config(package_Path)
    contain_Shell_Config = list()
    zh_Pattern = re.compile(u'[\u4e00-\u9fa5]+')
    i = 0
    for i in range(len(all_Shell_Config)):
        sfile = open(all_Shell_Config[i], 'rb')
        line = sfile.readline()
        try:
            uline = line.decode('utf-8')
        except Exception:
            contain_Shell_Config.append(all_Shell_Config[i])
            break
        while line:
            match = zh_Pattern.search(uline)
            if match:
                contain_Shell_Config.append(all_Shell_Config[i])
                break
            else:
                line = sfile.readline()
                try:
                    uline = line.decode('utf-8')
                except Exception:
                    contain_Shell_Config.append(all_Shell_Config[i])
                    break

        i += 1

    return contain_Shell_Config