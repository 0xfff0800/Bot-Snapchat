# Add project root to sys.path before any import
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# python3 -m venv myenv
from time import sleep
from appium import webdriver
from appium.options.ios import XCUITestOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import datetime
import pytz
import random
import sys
import base64
from app import db, DeviceStatus
from app import create_app  # استدعِ دالة إنشاء التطبيق
app = create_app()
from datetime import datetime


def mark_device_busy(udid):
    with app.app_context():
        device = DeviceStatus.query.filter_by(udid=udid).first()
        if device:
            device.status = "مشغول"
            device.last_updated = datetime.utcnow()
            db.session.commit()

def mark_device_available(udid):
    with app.app_context():
        device = DeviceStatus.query.filter_by(udid=udid).first()
        if device:
            device.status = "متاح"
            device.last_updated = datetime.utcnow()
            db.session.commit()


user = sys.argv[1] if len(sys.argv) > 1 else "unknown_user"

saudi_tz = pytz.timezone('Asia/Riyadh')
now = datetime.now(saudi_tz)
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")


with open("data/messages.txt", "r", encoding="utf-8") as f:
    messages = f.readlines()

random_message = random.choice(messages).strip()


options = XCUITestOptions()
options.platform_name = 'iOS'
options.platform_version = '15.7.5'
options.device_name = 'iphone'
options.automation_name = 'XCUITest'
options.udid = 'your-device-udid'
options.bundle_id = 'com.toyopagroup.picaboo'  # Snapchat
options.xcode_org_id = 'your-org-id' 
options.xcode_signing_id = 'iPhone Developer'
options.use_new_wda = True
options.no_reset = True

mark_device_busy(options.udid)

driver = webdriver.Remote(
    command_executor='http://127.0.0.1:4723',
    options=options
)


driver.implicitly_wait(2)
log_file = open("data/result.txt", "w")


try:
    login_button = driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="ngs_search_button"]')
    login_button.click()
    #print("✅ 1")
except:
    print("❌ 1 ")


try:
    scsig_tbt_button = driver.find_element(By.XPATH, '//XCUIElementTypeTextField[@name="search-textfield"]')
    scsig_tbt_button.click()
    scsig_tbt_button.send_keys(f"{user}")
    driver.start_recording_screen()
    #print("🔴 بدأ تسجيل الشاشة")
    #print("2")
except:
    print("❌ 2")


try:
    Entry_button = driver.find_element(By.XPATH, '(//XCUIElementTypeOther[@name="avatar"])[1]/XCUIElementTypeImage')
    Entry_button.click()
    #print("✅ 3")
except:
    Entry_button = driver.find_element(By.XPATH, '//XCUIElementTypeOther[@name="user-result-cell"]')
    Entry_button.click()
    print("❌ 3")


try:
    draw_button = driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="profile"]')
    draw_button.click()
    #print("✅ 4")
except:
    print("❌ 4")

try:
    Entry_button = driver.find_element(By.XPATH, '//XCUIElementTypeOther[@name="unified_profile_icon_button_action_menu"]')
    Entry_button.click()
    #print("✅ 5")
except:
    print("❌ 5")

try:
    Entry_button = driver.find_element(By.XPATH, '(//XCUIElementTypeOther[@name="unified_action_menu_item"])[3]')
    Entry_button.click()
    #print("✅ 6")
except:
    print("❌ 6")

try:
    Entry_button = driver.find_element(By.XPATH, '(//XCUIElementTypeOther[@name="in_app_reporting_core/list_reason_item"])[1]')
    Entry_button.click()
    #print("✅ 7")
except:
    print("❌ 7")

try:
    Entry_button = driver.find_element(By.XPATH, '(//XCUIElementTypeOther[@name="in_app_reporting_core/list_reason_item"])[4]')
    Entry_button.click()
    #print("✅ 8")
except:
    print("❌ 8")

try:
    Entry_button = driver.find_element(By.XPATH, '//XCUIElementTypeTextView[@name="in_app_reporting_core/comment_textfield"]')
    Entry_button.click()
    Entry_button.send_keys(random_message)
    #print("✅ 9")
except:
    print("❌ 9")

try:
    Entry_button = driver.find_element(By.XPATH, '//XCUIElementTypeOther[@name="in_app_reporting_core/submit_button"]')
    Entry_button.click()
    #print("✅ 10")
except:
    print("❌ 10")

try:
    Entry_button = driver.find_element(By.XPATH, '//XCUIElementTypeOther[@name="in_app_reporting_core/submit_done_button"]')
    Entry_button.click()
    #print("✅ 11")
except:
    print("❌ 11")


sleep(3)

raw_video = driver.stop_recording_screen()
print("📦 تم استلام البيانات")
video_path = os.path.join(os.path.dirname(__file__), '..', 'data', f"{user}_report.mp4")

with open(video_path, "wb") as f:
    f.write(base64.b64decode(raw_video))
    print("📝 جاري تشغيل الشاشة")

print(f"🎥 رابط الفيديو: https://ad13-2001-16a2-4536-7800-d50f-27fd-44ad-3aed.ngrok-free.app/video/{user}_report.mp4")

log_file.write(f"{formatted_time} - {user} was reported\n")
log_file.close()
driver.terminate_app("com.toyopagroup.picaboo")
driver.quit()

mark_device_available(options.udid)

print("👋 تمت الجلسة بالكامل")