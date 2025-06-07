from app import create_app, db
from app.models import DeviceStatus
from datetime import datetime

app = create_app()

with app.app_context():
    # تحقق إن كان الجهاز مضاف مسبقًا
    udid = "your-device-udid"  # استبدل بـ UDID الخاص بجهازك
    existing = DeviceStatus.query.filter_by(udid=udid).first()
    if not existing:
        device = DeviceStatus(
            udid=udid,
            name="iPhone",
            platform_name="iOS",
            platform_version="15.7.5",
            app_running="com.toyopagroup.picaboo",
            status="متاح",
            estimated_finish="",
            last_updated=datetime.utcnow()
        )
        db.session.add(device)
        db.session.commit()
        print("✅ تمت إضافة الجهاز إلى قاعدة البيانات.")
    else:
        print("ℹ️ الجهاز موجود مسبقًا.")