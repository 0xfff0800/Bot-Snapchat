

import os
import base64
from flask import Flask, send_file, jsonify, Blueprint
from threading import Thread
import time
from appium import webdriver
from appium.options.ios import XCUITestOptions

screen_bp = Blueprint('screen', __name__)
video_file = "latest_recording.mp4"

def record_screen():
    options = XCUITestOptions()
    options.platform_name = 'iOS'
    options.platform_version = '15.7.5'
    options.device_name = 'iPhone'
    options.automation_name = 'XCUITest'
    options.udid = 'a28bcf2593a3126dc98aa5098e461ea3784f1eab'
    options.bundle_id = 'com.toyopagroup.picaboo'
    options.xcode_org_id = 'GLBVL5TD9Q'
    options.xcode_signing_id = 'iPhone Developer'
    options.no_reset = True

    driver = webdriver.Remote(
        command_executor='http://127.0.0.1:4723',
        options=options
    )

    driver.start_recording_screen()
    print("🔴 بدء التسجيل...")

    time.sleep(20)

    raw_data = driver.stop_recording_screen()
    with open(video_file, "wb") as f:
        f.write(base64.b64decode(raw_data))

    print("✅ تم حفظ التسجيل في:", video_file)
    driver.quit()

@screen_bp.route('/start-recording')
def start_recording():
    thread = Thread(target=record_screen)
    thread.start()
    return jsonify({"status": "recording started"}), 200

@screen_bp.route("/video/<filename>")
def serve_named_video(filename):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    file_path = os.path.join(base_dir, filename)

    if os.path.exists(file_path):
        return send_file(file_path, mimetype='video/mp4')
    else:
        return jsonify({"error": f"Video not found"}), 404
    
