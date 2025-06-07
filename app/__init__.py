import subprocess
from flask import Flask, render_template, request, jsonify
from .spotlight_routes import spotlight_bp
from .report_api import report_bp
from .screen_routes import screen_bp
from .custom_request_routes import custom_request_bp
from flask_cors import CORS
from .extensions import db, migrate  
from flask_sqlalchemy import SQLAlchemy
import os
from . import models  
from .extensions import migrate  
from .models import DeviceStatus
from .models import APIKey 
from .strak_roures import Strak_bp

def create_app():
    app = Flask(__name__)
    db_path = os.path.join(os.path.dirname(__file__), '..', 'db', 'data.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(report_bp)
    app.register_blueprint(spotlight_bp)
    app.register_blueprint(screen_bp)
    app.register_blueprint(custom_request_bp)
    app.register_blueprint(Strak_bp)

    @app.route("/")
    def dashboard():
        device = DeviceStatus.query.first()
        return render_template("dashboard.html", device_status=device.status if device else "غير معروف")

    @app.route("/Report.Snapchat")
    def report_snapchat():
        return render_template("Report.Snapchat.html")

    @app.route("/Story.Snapchat")
    def spotlight():
        return render_template("Story.Spotlight.html")

    @app.route("/Strak.Snapchat")
    def Strak():
        return render_template("Strak.Snapchat.html")

    @app.route("/Custom.Service", methods=["GET", "POST"])
    def custom_service():
        return render_template("Custom.Service.html")
    
    @app.route("/success")
    def success():
        return render_template("success.html")
    @app.route('/api/add_key', methods=['POST'])
    def add_api_key():
        data = request.get_json()

        key = data.get('key')
        credits = data.get('credits', 0)

        if not key:
            return jsonify({'error': 'مطلوب إدخال المفتاح'}), 400

        if APIKey.query.filter_by(key=key).first():
            return jsonify({'error': '🔐 المفتاح موجود مسبقًا'}), 400

        new_key = APIKey(key=key, credits=credits)
        db.session.add(new_key)
        db.session.commit()

        return jsonify({'message': '✅ تم إنشاء المفتاح بنجاح'})

    @app.route("/device-status")
    def device_status():
        device = DeviceStatus.query.first()
        if not device:
            return jsonify({"error": "Device not found"}), 404

        return jsonify({
        "device": device.device_name,
        "status": device.status,
        "estimated_finish": device.estimated_finish
        })

    @app.route('/Telegraph.Post', methods=['GET', 'POST'])
    def send_post():
        message = None
        video_path = None

        if request.method == 'POST':
            device = DeviceStatus.query.first()
            if device and device.status != "متاح":
                message = "❌ الجهاز غير متاح حاليًا، الرجاء المحاولة لاحقًا"
                video_txt_path = os.path.join("latest_video.txt")
                if os.path.exists(video_txt_path):
                    with open(video_txt_path, 'r') as f:
                        video_filename = f.read().strip()
                        video_path = f"/data/{video_filename}"
                return render_template("Telegraph.html", message=message, video_url=video_path)
            
            username = request.form['username']
            post_url = request.form['post_url']
            with open("scripts/telegram_config.txt", "w") as f:
                f.write(f"{username}\n{post_url}")
            subprocess.Popen(["python3", "scripts/telegram_download.py"])
            message = "✅ جاري تحميل البوست بنجاح، الرجاء الانتظار قليلاً"

        video_txt_path = os.path.join("latest_video.txt")
        if os.path.exists(video_txt_path):
            with open(video_txt_path, 'r') as f:
                video_filename = f.read().strip()
                video_path = f"/data/{video_filename}"

        return render_template("Telegraph.html", message=message, video_url=video_path)
         
    return app