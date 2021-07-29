import CheckContain, xlwt

workbook = xlwt.Workbook()

def test_AnybackupClient_Linux7():
    package_Path = '/Packages/AnyBackupClient-Linux7/'
    contain_Shell_Config = CheckContain.Is_Chinese_Contain(package_Path)
    sheet01 = workbook.add_sheet("AnyBackupClient-Linux7")
    i = 0
    for i in range(len(contain_Shell_Config)):
        sheet01.write(i, 0, 'AnyBackupClient-Linux7')
        sheet01.wirte(i, 1, contain_Shell_Config[i])
        sheet01.write(i, 2, u'该文件中包含中文字符')

    sheet01.col(0).width = 256*20
    sheet01.col(1).width = 256*80
    sheet01.col(2).witdh = 256*50
    workbook.save("/Run/workspace/客户端包中文字符检测情况.xls")

def test_AnybackupClient_Linuxaarch():
    package_Path = '/Packages/AnyBackupClient-Linuxaarch/'
    contain_Shell_Config = CheckContain.Is_Chinese_Contain(package_Path)
    sheet02 = workbook.add_sheet("AnyBackupClient-Linuxaarch")
    i = 0
    for i in range(len(contain_Shell_Config)):
        sheet02.write(i, 0, 'AnyBackupClient-Linuxaarch')
        sheet02.wirte(i, 1, contain_Shell_Config[i])
        sheet02.write(i, 2, u'该文件中包含中文字符')

    sheet02.col(0).width = 256*20
    sheet02.col(1).width = 256*80
    sheet02.col(2).witdh = 256*50
    workbook.save("/Run/workspace/客户端包中文字符检测情况.xls")

def test_AnybackupClient_NeoKylin():
    package_Path = '/Packages/AnyBackupClient-NeoKylin/'
    contain_Shell_Config = CheckContain.Is_Chinese_Contain(package_Path)
    sheet02 = workbook.add_sheet("AnyBackupClient-NeoKylin")
    i = 0
    for i in range(len(contain_Shell_Config)):
        sheet02.write(i, 0, 'AnyBackupClient-NeoKylin')
        sheet02.wirte(i, 1, contain_Shell_Config[i])
        sheet02.write(i, 2, u'该文件中包含中文字符')

    sheet02.col(0).width = 256*20
    sheet02.col(1).width = 256*80
    sheet02.col(2).witdh = 256*50
    workbook.save("/Run/workspace/客户端包中文字符检测情况.xls")

def test_AnybackupClient_AIX():
    package_Path = '/Packages/AnyBackupClient-AIX/'
    contain_Shell_Config = CheckContain.Is_Chinese_Contain(package_Path)
    sheet04 = workbook.add_sheet("AnyBackupClient-AIX")
    i = 0
    for i in range(len(contain_Shell_Config)):
        sheet04.write(i, 0, 'AnyBackupClient-AIX')
        sheet04.wirte(i, 1, contain_Shell_Config[i])
        sheet04.write(i, 2, u'该文件中包含中文字符')

    sheet04.col(0).width = 256*20
    sheet04.col(1).width = 256*80
    sheet04.col(2).witdh = 256*50
    workbook.save("/Run/workspace/客户端包中文字符检测情况.xls")

def test_AnybackupClient_HPUX():
    package_Path = '/Packages/AnyBackupClient-HPUX/'
    contain_Shell_Config = CheckContain.Is_Chinese_Contain(package_Path)
    sheet06 = workbook.add_sheet("AnyBackupClient-HPUX")
    i = 0
    for i in range(len(contain_Shell_Config)):
        sheet06.write(i, 0, 'AnyBackupClient-HPUX')
        sheet06.wirte(i, 1, contain_Shell_Config[i])
        sheet06.write(i, 2, u'该文件中包含中文字符')

    sheet06.col(0).width = 256*20
    sheet06.col(1).width = 256*80
    sheet06.col(2).witdh = 256*50
    workbook.save("/Run/workspace/客户端包中文字符检测情况.xls")

def test_AnybackupClient_Linux8():
    package_Path = '/Packages/AnyBackupClient-Linux8/'
    contain_Shell_Config = CheckContain.Is_Chinese_Contain(package_Path)
    sheet07 = workbook.add_sheet("AnyBackupClient-Linux8")
    i = 0
    for i in range(len(contain_Shell_Config)):
        sheet07.write(i, 0, 'AnyBackupClient-Linux8')
        sheet07.wirte(i, 1, contain_Shell_Config[i])
        sheet07.write(i, 2, u'该文件中包含中文字符')

    sheet07.col(0).width = 256*20
    sheet07.col(1).width = 256*80
    sheet07.col(2).witdh = 256*50
    workbook.save("/Run/workspace/客户端包中文字符检测情况.xls")

def test_AnybackupClient_Redhat5():
    package_Path = '/Packages/AnyBackupClient-Redhat5/'
    contain_Shell_Config = CheckContain.Is_Chinese_Contain(package_Path)
    sheet08 = workbook.add_sheet("AnyBackupClient-Redhat5")
    i = 0
    for i in range(len(contain_Shell_Config)):
        sheet08.write(i, 0, 'AnyBackupClient-Redhat5')
        sheet08.wirte(i, 1, contain_Shell_Config[i])
        sheet08.write(i, 2, u'该文件中包含中文字符')

    sheet08.col(0).width = 256*20
    sheet08.col(1).width = 256*80
    sheet08.col(2).witdh = 256*50
    workbook.save("/Run/workspace/客户端包中文字符检测情况.xls")

def test_AnybackupClient_Windowsi386():
    package_Path = '/Packages/AnyBackupClient-Windowsi386/'
    contain_Shell_Config = CheckContain.Is_Chinese_Contain(package_Path)
    sheet09 = workbook.add_sheet("AnyBackupClient-Windowsi386")
    i = 0
    for i in range(len(contain_Shell_Config)):
        sheet09.write(i, 0, 'AnyBackupClient-Windowsi386')
        sheet09.wirte(i, 1, contain_Shell_Config[i])
        sheet09.write(i, 2, u'该文件中包含中文字符')

    sheet09.col(0).width = 256*20
    sheet09.col(1).width = 256*80
    sheet09.col(2).witdh = 256*50
    workbook.save("/Run/workspace/客户端包中文字符检测情况.xls")

def test_AnybackupClient_Windowsx64():
    package_Path = '/Packages/AnyBackupClient-Windowsx64/'
    contain_Shell_Config = CheckContain.Is_Chinese_Contain(package_Path)
    sheet10 = workbook.add_sheet("AnyBackupClient-Windowsx64")
    i = 0
    for i in range(len(contain_Shell_Config)):
        sheet10.write(i, 0, 'AnyBackupClient-Windowsx64')
        sheet10.wirte(i, 1, contain_Shell_Config[i])
        sheet10.write(i, 2, u'该文件中包含中文字符')

    sheet10.col(0).width = 256*20
    sheet10.col(1).width = 256*80
    sheet10.col(2).witdh = 256*50
    workbook.save("/Run/workspace/客户端包中文字符检测情况.xls")

test_AnybackupClient_Linux7
test_AnybackupClient_Linuxaarch()
test_AnybackupClient_NeoKylin()
test_AnybackupClient_AIX()
test_AnybackupClient_HPUX()
test_AnybackupClient_Linux8()
test_AnybackupClient_Redhat5()
test_AnybackupClient_Windowsi386()
test_AnybackupClient_Windowsx64()