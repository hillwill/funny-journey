import time
import unittest2
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

class web_check(unittest2.TestCase):
    """登录admin，查看所有节点状态"""
    @classmethod
    def setUp(cls):
        # 打开浏览器
        cls.driver = webdriver.Chrome()
        # 将浏览器设置为占满整个屏幕
        cls.driver.maximize_window()
        # 访问网页
        cls.driver.get('https://10.4.8.6:9600')
        cls.driver.implicitly_wait(5)

    def test_openit(self):
        """访问控制台"""
        # admin登录
        self.driver.find_element_by_name("userName").send_keys("admin")
        self.driver.find_element_by_name("password").send_keys("EISOO.COM123")
        self.driver.find_element_by_xpath("//*[@id='app']/div[2]/div/ng-include/div/div/div/form/div[2]/button").click()
        time.sleep(3)
        self.driver.find_element_by_xpath("//*[contains(text(), '确定')]").click()
        time.sleep(1)
        # 查看节点状态
        self.driver.find_element_by_link_text("存储").click()
        self.driver.find_element_by_link_text("节点管理").click()
        time.sleep(5)
        self.driver.find_element_by_class_name("logout").click()
        time.sleep(2)
        self.driver.find_element_by_css_selector('.btn.btn-es-red.ng-scope').click()
        print("admin登录成功，节点状态正常！")
        time.sleep(3)

        # sadmin登录
        self.driver.find_element_by_name("userName").send_keys("sadmin")
        self.driver.find_element_by_name("password").send_keys("EISOO.COM123")
        self.driver.find_element_by_xpath("//*[@id='app']/div[2]/div/ng-include/div/div/div/form/div[2]/button").click()
        time.sleep(3)
        self.driver.find_element_by_xpath("//*[contains(text(), '确定')]").click()
        time.sleep(1)
        # 查看用户日志和任务日志
        self.driver.find_element_by_link_text("日志").click()
        self.driver.find_element_by_link_text("用户日志").click()
        time.sleep(5)
        self.driver.find_element_by_link_text("任务日志").click()
        time.sleep(5)
        self.driver.find_element_by_class_name("logout").click()
        time.sleep(2)
        print("sadmin登录成功，查看用户日志和任务日志正常！")
        self.driver.find_element_by_css_selector('.btn.btn-es-red.ng-scope').click()
        time.sleep(3)

        # 操作员登录
        self.driver.find_element_by_name("userName").send_keys("newer")
        self.driver.find_element_by_name("password").send_keys("EISOO.COM123")
        self.driver.find_element_by_xpath("//*[@id='app']/div[2]/div/ng-include/div/div/div/form/div[2]/button").click()
        time.sleep(3)
        self.driver.find_element_by_xpath("//*[contains(text(), '确定')]").click()
        time.sleep(1)
        # 编辑任务
        self.driver.find_element_by_link_text("定时数据保护").click()
        self.driver.find_element_by_link_text("数据备份").click()
        self.driver.find_element_by_xpath("//*[contains(text(), 'test1')]").click()
        time.sleep(1)
        self.driver.find_element_by_link_text("编辑").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[contains(text(), '下一步')]").click()
        self.driver.find_element_by_xpath("//*[contains(text(), '下一步')]").click()
        self.driver.find_element_by_xpath("//*[contains(text(), '下一步')]").click()
        el = self.driver.find_element_by_xpath("//*[@id='content']/section/div/div/div/es-wizard/div/div/div[3]/button[3]")
        el.send_keys(Keys.ENTER)
        time.sleep(6)
        self.driver.find_element_by_class_name("logout").click()
        time.sleep(3)
        self.driver.find_element_by_css_selector('.btn.btn-es-red.ng-scope').click()
        time.sleep(2)
        print("操作员登录成功，编辑任务正常！")
        time.sleep(5)

    @classmethod
    def tearDown(cls):
        cls.driver.close()

if __name__ == '__main__':
    unittest2.main()