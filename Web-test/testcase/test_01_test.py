#测试用户设置策略配置/发起自备份/下载自备份到本地
import time
from nose_parameterized import parameterized,param
from  selenium import webdriver
import unittest2
import os

class Createuser(unittest2.TestCase):
    """"新建管理员和操作员"""
    def setUp(cls):
        cls.driver=webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(5)
        cls.test_ip = "10.2.22.61"
        cls.product_id = "7.0.8.0"
        cls.path = os.getcwd()
        cls.driver.get("https://10.2.12.159:9600")
        cls.driver.find_element_by_name("userName").send_keys("test")
        cls.driver.find_element_by_name("password").send_keys("eisoo.com123")
        cls.driver.find_element_by_xpath("//*[@id='app']/div[2]/div/ng-include/div/div/div/form/div[2]/button").click()
        time.sleep(5)

    @parameterized.expand([
        param("wxt"),
    ])
    def test_createuser(self, newoperator):
        """"新建操作员"""
        # self.driver.find_element_by_xpath("//*[@id='ngdialog8']/div[2]/div[3]/button[1]").click()
        # self.driver.find_element_by_xpath("/html/body/div[2]/div/section/div[2]/div[2]/div[3]/button[1]").click()
        self.driver.find_element_by_name("usermgm").click()
        # self.driver.find_element_by_css_selector('#content > div > div > ht-sidebar > div > ul > li:nth-child(2) > ul > li:nth-child(1)').click()
        # time.sleep(3)
        # self.driver.find_element_by_css_selector('#content > section > div > div > div > div > div > ul > li:nth-child(3) > a > uib-tab-heading').click()
        # self.driver.find_element_by_css_selector('#content > section > div > div > div > div > div > div > div.tab-pane.ng-scope.active > div > div > div > div > div.es-grid-toolbar.user-page > div.pull-left > a.btn.btn-es-reverse.btn-sm.margin-control.ng-scope').click()
        # time.sleep(3)
        # self.driver.find_element_by_name('userName').send_keys(newoperator)
        # time.sleep(2)
        # self.driver.find_element_by_css_selector('.content-footer > :nth-child(1)').click()
        # print(newoperator+u"操作员新建成功")
    def tearDown(cls):
        cls.driver.close()


if __name__ == '__main__':
    unittest2.main()