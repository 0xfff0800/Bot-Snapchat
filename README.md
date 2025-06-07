# 🤖 Bot-Snapchat-Appium

**Experimental version of an intelligent system that runs on iOS to control the Snapchat app automatically using Appium.**

## 📱 Overview

Bot-Snapchat-Appium is a smart automation system designed to control the Snapchat app on a real iPhone device **without jailbreak**. It leverages **Appium + Flask Web Server** to automate tasks through a smart bot connected to a private network.

### ▶️ Demo Video

Watch the demo on YouTube:

[![Watch the video](https://img.youtube.com/vi/mifjeCzySKo/0.jpg)](https://www.youtube.com/watch?v=mifjeCzySKo)

---

### ⚙️ Key Features

* ✅ Automatically send Streaks to all friends or groups.
* ✅ Support for sending Stories to Spotlight or personal story.
* ✅ Download videos from Telegram links (channels / groups / private chats).
* ✅ Automatically share Telegram content to Snapchat.
* ✅ Automatically record the screen for each step (complete process documentation).
* ✅ Session and device management (Available / Busy).
* ✅ Easily customizable per client requirements.

---

## 🧪 Current Status

> This version is **experimental** and intended for testing only. Requests can be submitted via WhatsApp or Telegram to try the service and contribute to its development.

---

## 🚀 How to Use

### 📦 Requirements

* 🐍 Python 3.x
* 🔧 Appium
* 🧪 Xcode (macOS)
* 🌐 Ngrok
* 📱 Real iPhone connected via USB

### 🛠️ Setup Steps

1. Connect a real iOS device via USB.

2. Start Appium server:

```bash
appium
```

3. Run Flask server:

```bash
python3 -m flask run --host=0.0.0.0 --port=8000
```

4. Start Ngrok to expose Flask API:

```bash
ngrok http 8000
```

5. *(Optional)* For fast execution (e.g., sending quick Streaks without using the web interface):

```bash
python3 scripts/Strak_Snapchat.py "Story text" "username"
```

6. *(Optional)* Add new API keys using a POST request:

```bash
curl -X POST http://127.0.0.1:8000/api/add_key \
     -H "Content-Type: application/json" \
     -d '{
           "key": "sk_live_1234567890abcdef",
           "credits": 50
         }'
```

### 📌 Important Notes

* Modify device configuration inside scripts (`report.py`, `story_spotlight.py`, `Strak_Snapchat.py`) in this section:

```python
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
```

* After starting ngrok, **manually update the public URL** in the following files:

  * `Report.Snapchat.html`
  * `Story.Spotlight.html`
  * `Strak.Snapchat.html`
  * `report.py`
  * `story_spotlight.py`
  * `Strak_Snapchat.py`

---

## 📩 Contact

To request the service or contribute to its development:

📨 Telegram : [Click here](https://t.me/flaah999)
