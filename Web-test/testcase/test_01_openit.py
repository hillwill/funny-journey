import time
import unittest2
from parameterized import parameterized, param
from selenium import webdriver

class openit(unittest2.TestCase):
    def setUp(cls):
        # 打开浏览器
        cls.driver = webdriver.Chrome()
        # 将浏览器设置为占满整个屏幕
        cls.driver.maximize_window()
        # 访问网页
        cls.driver.get('https://10.2.12.159:9600')
        # 等待
        time.sleep(5)
        # 刷新
        # cls.driver.refresh()
        # cls.driver.get_screenshot_as_file("D:\\b.jpg")
        # time.sleep(5)
        cls.driver.find_element_by_name("userName").send_keys("test")
        cls.driver.find_element_by_name("password").send_keys("xxx123")
        # cls.driver.find_element_by_css_selector('#app > div.login.ng-scope > div > ng-include > div > div > div > form > div.login-form-container > button') .click()
        cls.driver.find_element_by_xpath("//*[@id='app']/div[2]/div/ng-include/div/div/div/form/div[2]/button")
        time.sleep(5)

    @parameterized.expand([
        param("xxx"),
    ])
    def test_createuser(self, newoperator):
        """"新建操作员"""

    def tearDown(cls):
        cls.driver.close()

if __name__ == '__main__':
    unittest2.main()
