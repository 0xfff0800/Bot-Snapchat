# python3 -m venv myenv
import base64
import os
from time import sleep
from appium import webdriver
from appium.options.ios import XCUITestOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import datetime
import pytz
import random
import sys
import datetime
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import db, DeviceStatus
from app import create_app

app = create_app()
app.app_context().push()


text = sys.argv[1] if len(sys.argv) > 1 else "unknown_text"
user = sys.argv[2] if len(sys.argv) > 2 else "unknown_user"

saudi_tz = pytz.timezone('Asia/Riyadh')
now = datetime.datetime.now(saudi_tz)
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

# إعداد خيارات Appium
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


def mark_device_busy(udid):
    device = DeviceStatus.query.filter_by(udid=udid).first()
    if device:
        device.status = "مشغول"
        device.last_updated = datetime.datetime.utcnow()
        db.session.commit()

mark_device_busy(options.udid)

# الاتصال بخادم Appium
driver = webdriver.Remote(
    command_executor='http://127.0.0.1:4723',
    options=options
)

print("✅ تم فتح Snapchat على الجهاز")

driver.implicitly_wait(2)
log_file = open("data/result.txt", "w")

def mark_device_available(udid):
    device = DeviceStatus.query.filter_by(udid=udid).first()
    if device:
        device.status = "متاح"
        device.last_updated = datetime.datetime.utcnow()
        db.session.commit()

try:
    login_button = driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="share_from_memories"]')
    login_button.click()
    print("✅ ايقونه البوم الصور")
except:
    print("❌ لم يتم العثور على زر البوم الصور")


try:
    scsig_tbt_button = driver.find_element(By.XPATH, '//XCUIElementTypeStaticText[@name="scsig_tbt" and @label="⁧ألبوم الكاميرا⁩"]')
    scsig_tbt_button.click()
    driver.start_recording_screen()
    print("✅ ألبوم الكاميرا⁩")
except:
    print("❌ لم يتم العثور على ألبوم الكاميرا⁩")


try:
    Entry_button = driver.find_element(By.XPATH, '//XCUIElementTypeCell[@name="Camera Roll Entry: 0."]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeImage')
    Entry_button.click()
    print("✅ تم إختيار الفديو")
except:
    print("❌ لم يتم العثور على الفديو")


try:
    draw_button = driver.find_element(By.XPATH, '//XCUIElementTypeOther[@name="caption"]/XCUIElementTypeImage')
    draw_button.click()
    draw_button.send_keys(f"{text}")
    print("✅ تم الضغط على زر الكتابة")
except:
    print("❌ لم يتم العثور على زر الكتابة")

try:
    Entry_button = driver.find_element(By.XPATH, '//XCUIElementTypeOther[@name="camera_roll_tab"]/XCUIElementTypeOther[1]/XCUIElementTypeOther')
    Entry_button.click()
    print("✅ تم الضغط علي الشاشه")
except:
    print("❌ لم يتم الضغط علي الشاشه")

# زر الارسال
try:
    Entry_button = driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="send_to_button"]')
    Entry_button.click()
    print("✅ زر الارسال")
except:
    print("❌ لم يتم الضغط علي زر الارسال")

# تحديد الكل
try:
    Entry_button = driver.find_element(By.XPATH, '(//XCUIElementTypeImage[@name="Cell_Select_Off"])[1]')
    Entry_button.click()
    print("✅ تحديد الكل")
except:
    print("❌ لم يتم الضغط علي زر تحديد الكل")


# زر ارسال
try:
    Entry_button = driver.find_element(By.XPATH, '//XCUIElementTypeImage[@name="Send_White"]')
    Entry_button.click()
    print("✅ زر الارسال")
except:
    print("❌ لم يتم الضغط علي زر الارسال")


# زر لاتحفظ التغيرات
try:
    Entry_button = driver.find_element(By.XPATH, '//XCUIElementTypeButton[@name="memories_preview_save_changes_dont_save"]')
    Entry_button.click()
    print("✅ زر لاتحفظ التغيرات")
except:
    print("❌ لم يتم الضغط علي زر لاتحفظ التغيرات")

sleep(3)
raw_video = driver.stop_recording_screen()
print("📦 تم استلام البيانات")
video_path = os.path.join(os.path.dirname(__file__), '..', 'data', f"{user}_store.mp4")

with open(video_path, "wb") as f:
    f.write(base64.b64decode(raw_video))
    print("📝 جاري تشغيل الشاشة")

print(f"🎥 رابط الفيديو: https://ad13-2001-16a2-4536-7800-d50f-27fd-44ad-3aed.ngrok-free.app/video/{user}_store.mp4")

log_file.write(f"{formatted_time} - {user} - {text} ok add text\n")
log_file.close()
driver.terminate_app("com.toyopagroup.picaboo")

mark_device_available(options.udid)

driver.quit()


