import os
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from time import sleep
from processor import Processor
from config import *


class Moments():
    def __init__(self):
        """
        初始化
        """
        # 驱动配置
        self.desired_caps = {
            'platformName': PLATFORM,
            'deviceName': DEVICE_NAME,
            'appPackage': APP_PACKAGE,
            'appActivity': APP_ACTIVITY,
            'noReset': NORESET
        }
        self.driver = webdriver.Remote(DRIVER_SERVER, self.desired_caps)
        self.wait = WebDriverWait(self.driver, TIMEOUT)
        self.client = MongoClient(MONGO_URL)
        self.db = self.client[MONGO_DB]
        self.collection = self.db[MONGO_COLLECTION]
        # 处理器
        self.processor = Processor()
    
    def login(self):
        """
        登录微信
        :return:
        """
        # 登录按钮
        login = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/d1w')))
        login.click()
        # 手机输入
        phone = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/hx')))
        phone.set_text(USERNAME)
        # 下一步
        next = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/ak_')))
        next.click()
        # 密码
        password = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@resource-id="com.tencent.mm:id/hx"][1]')))
        password.set_text(PASSWORD)
        # 提交
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/ak_')))
        submit.click()
    
    def enter(self):
        """
        进入朋友圈
        :return:
        """
        # 发现
        # tab = self.wait.until(
        #     EC.presence_of_element_located((By.XPATH, '//*[@resource-id="com.tencent.mm:id/ayn"][3]')))
        # tab.click()

        # 没找到发现在哪-.-
        moments = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/gz')))
        TouchAction(self.driver).tap(x=870, y=2618).perform()

        # 朋友圈
        moments = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/a9d')))
        moments.click()
    
    def crawl(self):
        """
        爬取
        :return:
        """
        while True:
            # 当前页面显示的所有状态
            items = self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//*[@resource-id="com.tencent.mm:id/dgn"]//android.widget.FrameLayout')))
            # 上滑
            self.driver.swipe(FLICK_START_X, FLICK_START_Y + FLICK_DISTANCE, FLICK_START_X, FLICK_START_Y)
            # 遍历每条状态
            for item in items:
                try:
                    # 昵称
                    nickname = item.find_element_by_id('com.tencent.mm:id/apv').get_attribute('text')

                    # 正文
                    content = item.find_element_by_id('com.tencent.mm:id/deq').get_attribute('text')


                    # 日期我又没找到, 不知道微信藏哪了
                    # # 日期
                    # date = item.find_element_by_id('com.tencent.mm:id/dag').get_attribute('text')
                    # # 处理日期
                    # date = self.processor.date(date)

                    if nickname != 'zxc': # 我的微信昵称
                        # print(nickname, content)
                        data = {
                            'nickname': nickname,
                            'content': content,
                            # 'date': date,
                        }
                        print(data)
                        # 插入MongoDB
                        self.collection.update({'nickname': nickname, 'content': content}, {'$set': data}, True)
                        sleep(SCROLL_SLEEP_TIME)
                except NoSuchElementException:
                    pass
    
    def main(self):
        """
        入口
        :return:
        """
        # 登录
        # self.login()
        # 进入朋友圈
        self.enter()
        # 爬取
        self.crawl()


if __name__ == '__main__':
    moments = Moments()
    moments.main()