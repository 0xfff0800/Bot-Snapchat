from flask import Blueprint, request, jsonify
import subprocess
from app.models import APIKey
from app.extensions import db
from .models import DeviceStatus

Strak_bp = Blueprint('Strak_bp', __name__)

def get_api_key_info(key):
    return APIKey.query.filter_by(key=key).first()

def deduct_credit(key):
    api_key = APIKey.query.filter_by(key=key, active=True).first()
    if api_key and api_key.credits > 0:
        api_key.credits -= 1
        db.session.commit()

@Strak_bp.route('/Strak_post', methods=['POST'])
def post_spotlight():
    data = request.json
    username = data.get('username')

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

    if not username:
        return jsonify({"error": "username is required"}), 400

    result = subprocess.run(
        ["python3", "scripts/Strak_Snapchat.py", username],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return jsonify({
            "error": "Script execution failed",
        }), 500

    deduct_credit(auth)

    return jsonify({
        "status": "done",
        "output": result.stdout,
        "remaining_credits": key_info.credits
    })