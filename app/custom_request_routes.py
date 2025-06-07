from flask import Blueprint, request, jsonify
from .extensions import db  # ✅ بدّل الاستيراد
from .models import CustomRequest

custom_request_bp = Blueprint('custom_request', __name__)

@custom_request_bp.route('/submit-custom-request', methods=['POST'])
def submit_custom_request():
    data = request.get_json()

    required_fields = ['platform', 'feature', 'os_version', 'jailbreak_status', 'contact_info']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400

    new_request = CustomRequest(
        platform=data['platform'],
        feature=data['feature'],
        os_version=data['os_version'],
        jailbreak_status=data['jailbreak_status'],
        notes=data.get('notes', ''),
        contact_info=data['contact_info'],
        status='قيد المراجعة'
    )
    db.session.add(new_request)
    db.session.commit()

    return jsonify({'message': 'تم إرسال الطلب بنجاح'})