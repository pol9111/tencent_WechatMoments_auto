from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

server = 'http://localhost:4723/wd/hub'

desired_caps = {
    'platformName': 'Android',
    'deviceName': 'SM_G9500',
    'appPackage': 'com.tencent.mm',
    'appActivity': '.ui.LauncherUI',
    'noReset': True # 启动app时不清除数据, 有些手机首次登入要询问授权, 设置True就不会出现了
}

# desired_caps = {
#     'platformName': 'Android',
#     'deviceName': 'MI_NOTE_Pro',
#     'app': './weixin.apk'
# }

driver = webdriver.Remote(server, desired_caps)
wait = WebDriverWait(driver, 30)
login = wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/d1w')))
# TouchAction(driver).tap(x=416, y=2592).perform()
login.click()
phone = wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/hx')))
phone.set_text('18888888888')


# TouchAction(driver).tap(x=416, y=2592).perform()
# el1 = driver.find_element_by_id("com.tencent.mm:id/hx")
# el1.send_keys("18950076568")
