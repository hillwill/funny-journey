import CheckContain, xlwt

workbook = xlwt.Workbook()

def test_AnybackupServer_Linux7():
    package_Path = '/Packages/AnyBackupServer-Linux7/'
    contain_Shell_Config = CheckContain.Is_Chinese_Contain(package_Path)
    sheet01 = workbook.add_sheet("AnyBackupServer-Linux7")
    i = 0
    for i in range(len(contain_Shell_Config)):
        sheet01.write(i, 0, 'AnybackupServer-Linux7')
        sheet01.wirte(i, 1, contain_Shell_Config[i])
        sheet01.write(i, 2, u'该文件中包含中文字符')

    sheet01.col(0).width = 256*20
    sheet01.col(1).width = 256*80
    sheet01.col(2).witdh = 256*50
    workbook.save("/Run/workspace/控制台包中文字符检测情况.xls")

def test_AnybackupServer_Linuxaarch():
    package_Path = '/Packages/AnyBackupServer-Linuxaarch/'
    contain_Shell_Config = CheckContain.Is_Chinese_Contain(package_Path)
    sheet02 = workbook.add_sheet("AnyBackupServer-Linuxaarch")
    i = 0
    for i in range(len(contain_Shell_Config)):
        sheet02.write(i, 0, 'AnyBackupServer-Linuxaarch')
        sheet02.wirte(i, 1, contain_Shell_Config[i])
        sheet02.write(i, 2, u'该文件中包含中文字符')

    sheet02.col(0).width = 256*20
    sheet02.col(1).width = 256*80
    sheet02.col(2).witdh = 256*50
    workbook.save("/Run/workspace/控制台包中文字符检测情况.xls")

def test_AnybackupServer_NeoKylin():
    package_Path = '/Packages/AnyBackupServer-NeoKylin/'
    contain_Shell_Config = CheckContain.Is_Chinese_Contain(package_Path)
    sheet03 = workbook.add_sheet("AnyBackupServer-NeoKylin")
    i = 0
    for i in range(len(contain_Shell_Config)):
        sheet03.write(i, 0, 'AnyBackupServer-NeoKylin')
        sheet03.wirte(i, 1, contain_Shell_Config[i])
        sheet03.write(i, 2, u'该文件中包含中文字符')

    sheet03.col(0).width = 256*20
    sheet03.col(1).width = 256*80
    sheet03.col(2).witdh = 256*50
    workbook.save("/Run/workspace/控制台包中文字符检测情况.xls")

def test_AnybackupServer_EKVM():
    package_Path = '/Packages/AnyBackupServer-EKVM/'
    contain_Shell_Config = CheckContain.Is_Chinese_Contain(package_Path)
    sheet04 = workbook.add_sheet("AnyBackupServer-EKVM")
    i = 0
    for i in range(len(contain_Shell_Config)):
        sheet04.write(i, 0, 'AnyBackupServer-EKVM')
        sheet04.wirte(i, 1, contain_Shell_Config[i])
        sheet04.write(i, 2, u'该文件中包含中文字符')

    sheet04.col(0).width = 256*20
    sheet04.col(1).width = 256*80
    sheet04.col(2).witdh = 256*50
    workbook.save("/Run/workspace/控制台包中文字符检测情况.xls")

test_AnybackupServer_Linux7()
test_AnybackupServer_Linuxaarch()
test_AnybackupServer_NeoKylin()
test_AnybackupServer_EKVM()