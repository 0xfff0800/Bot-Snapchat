import os
import sys
import base64
import datetime
import pytz
from time import sleep
from appium import webdriver
from appium.options.ios import XCUITestOptions
from selenium.webdriver.common.by import By

with open("scripts/telegram_config.txt", "r") as f:
    user = f.readline().strip()
    link = f.readline().strip()

options = XCUITestOptions()
options.platform_name = 'iOS'
options.platform_version = '15.7.5'
options.device_name = 'iphone'
options.automation_name = 'XCUITest'
options.udid = 'your-device-udid'
options.bundle_id = 'ph.telegra.Telegraph'  # Telegram
options.xcode_org_id = 'your-org-id'
options.xcode_signing_id = 'iPhone Developer'
options.use_new_wda = True
options.no_reset = True



driver = webdriver.Remote(
    command_executor='http://127.0.0.1:4723',
    options=options
)
driver.implicitly_wait(5)

# (Test) is the username that receives links in Telegram
try:
    channel = driver.find_element(By.XPATH, '//XCUIElementTypeOther[@name="Test"]')
    channel.click()
    sleep(2)
    input_field = driver.find_element(By.XPATH, '//XCUIElementTypeTextView')
    input_field.click()
    input_field.send_keys(link)
    sleep(1)
    send_button = driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="إرسال"]')
    send_button.click()
    sleep(2)
    extra_click = driver.find_element(By.XPATH, '//XCUIElementTypeApplication[@name="تيليجرام"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther[12]/XCUIElementTypeOther[1]/XCUIElementTypeOther')
    extra_click.click()
    sleep(2)
    dn_click = driver.find_element(By.XPATH, '//XCUIElementTypeApplication[@name="تيليجرام"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther')
    dn_click.click()
    sleep(0.5)
    driver.execute_script("mobile: tap", {"x": 23, "y": 642})
    sleep(2)
    input_field = driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="كِلا الصورتين"]')
    input_field.click()
    sleep(2)
    download_button = driver.find_element(By.XPATH, '//XCUIElementTypeWindow/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther[3]/XCUIElementTypeOther/XCUIElementTypeScrollView/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther[2]')
    download_button.click()
    sleep(2)
    # فتح سناب
    download_button = driver.find_element(By.XPATH, '//XCUIElementTypeCell[@name="Snapchat"]/XCUIElementTypeOther/XCUIElementTypeOther[1]')
    download_button.click()
except Exception as e:
    print(f"❌ Failed to send link: {e}")
    driver.quit()
    exit(1)


driver.quit()
os.system("python3 scripts/snapchat_send.py")
