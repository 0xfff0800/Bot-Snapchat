from datetime import datetime
from .extensions import db

class CustomRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(100))
    feature = db.Column(db.String(200))
    os_version = db.Column(db.String(100))
    jailbreak_status = db.Column(db.String(20))
    notes = db.Column(db.Text)
    contact_info = db.Column(db.String(200))
    status = db.Column(db.String(50), default='قيد المراجعة')

class APIKey(db.Model):
    __tablename__ = 'api_keys'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String, unique=True, nullable=False)
    credits = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)

class DeviceStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    udid = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    platform_name = db.Column(db.String(50))
    platform_version = db.Column(db.String(50))
    app_running = db.Column(db.String(100))
    status = db.Column(db.String(50), default='متاح')
    estimated_finish = db.Column(db.String(100))
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)