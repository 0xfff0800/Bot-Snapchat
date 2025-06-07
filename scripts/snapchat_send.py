from appium import webdriver
from appium.options.ios import XCUITestOptions
from selenium.webdriver.common.by import By
from time import sleep
import sys
import base64
import datetime
import os
import pytz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import db, DeviceStatus
from app import create_app

app = create_app()
app.app_context().push()


options = XCUITestOptions()
options.platform_name = 'iOS'
options.device_name = 'iphone'
options.automation_name = 'XCUITest'
options.udid = 'your-device-udid'
options.no_reset = True

def mark_device_busy(udid):
    device = DeviceStatus.query.filter_by(udid=udid).first()
    if device:
        device.status = "مشغول"
        device.last_updated = datetime.datetime.utcnow()
        db.session.commit()

mark_device_busy(options.udid)

driver = webdriver.Remote('http://127.0.0.1:4723', options=options)

def mark_device_available(udid):
    device = DeviceStatus.query.filter_by(udid=udid).first()
    if device:
        device.status = "متاح"
        device.last_updated = datetime.datetime.utcnow()
        db.session.commit()

print("✅ تم فتح Snapchat على الجهاز")
try:
    driver.start_recording_screen()
except Exception as e:
    print(f"❌ Failed to start recording: {e}")
    driver.quit()
    sys.exit(1)

download_button = driver.find_element(By.XPATH, '(//XCUIElementTypeOther[@name="SIGHeader"])[2]/XCUIElementTypeOther[1]')
download_button.click()

config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'telegram_config.txt'))
if not os.path.exists(config_path):
    print("❌ ملف التكوين telegram_config.txt غير موجود")
    driver.quit()
    sys.exit(1)

with open(config_path, 'r') as f:
    lines = f.read().splitlines()
    snapchat_username = lines[0] 

download_button.send_keys(snapchat_username)
sleep(1)
input_field = driver.find_element(By.XPATH, '//XCUIElementTypeImage[@name="Cell_Select_Off"]')
input_field.click()
sleep(1)
send_button = driver.find_element(By.XPATH, '//XCUIElementTypeOther[@name="send_button"]')
send_button.click()


try:
    video_raw = driver.stop_recording_screen()
except Exception as e:
    print(f"❌ Failed to stop recording: {e}")
    driver.quit()
    sys.exit(1)

saudi_tz = pytz.timezone('Asia/Riyadh')
now = datetime.datetime.now(saudi_tz)
timestamp = now.strftime("%Y%m%d_%H%M%S")
filename = f"snapchat_{timestamp}.mp4"
save_path = os.path.join(os.path.dirname(__file__), '..', 'data', filename)

with open(save_path, "wb") as f:
    f.write(base64.b64decode(video_raw))

try:
    os.remove(config_path)
except Exception as e:
    print(f"⚠️ لم يتم حذف telegram_config.txt: {e}")

with open(os.path.join(os.path.dirname(__file__), '..', 'latest_video.txt'), 'w') as f:
    f.write(filename)

print(f"✅ تم إرسال الفيديو بنجاح وحفظه في {save_path}")
driver.terminate_app("com.toyopagroup.picaboo")

mark_device_available(options.udid)
driver.quit()
