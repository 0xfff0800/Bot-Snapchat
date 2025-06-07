from flask import Blueprint, request, jsonify
import subprocess
from .models import APIKey
from .models import DeviceStatus

report_bp = Blueprint('report_bp', __name__)

def get_api_key_info(key):
    return APIKey.query.filter_by(key=key).first()

def deduct_credit(key):
    api_key = APIKey.query.filter_by(key=key, active=True).first()
    if api_key and api_key.credits > 0:
        api_key.credits -= 1
        from .extensions import db
        db.session.commit()

@report_bp.route('/report', methods=['POST'])
def report_user():
    auth = request.headers.get("Authorization")
    if not auth:
        return jsonify({"error": "Missing API key"}), 401

    key_info = get_api_key_info(auth)
    if not key_info:
        return jsonify({"error": "Invalid API key"}), 401

    credits = key_info.credits
    active = key_info.active

    device = DeviceStatus.query.first()
    if device and device.status == "مشغول":
        return jsonify({"error": "الجهاز مشغول حالياً، الرجاء المحاولة لاحقاً"}), 423

    if not active:
        return jsonify({"error": "API key is disabled"}), 403
    if credits <= 0:
        return jsonify({"error": "No credits remaining"}), 402

    data = request.json
    username = data.get("username")
    if not username:
        return jsonify({"error": "Missing username"}), 400

    result = subprocess.run(
        ["python3", "scripts/report.py", username],
        capture_output=True,
        text=True
    )


    if result.returncode != 0:
        return jsonify({
            "error": "Script execution failed",
        }), 500

    # خصم نقطة
    deduct_credit(auth)

    return jsonify({
        "status": "success",
        "used": username,
        "remaining_credits": credits - 1,
        "output": result.stdout
    })
