import logging
import os
import re
import subprocess

import cv2
import requests
from flask import Blueprint, render_template, redirect, url_for, session, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models import Device, User, Configure

main = Blueprint('main', __name__)

SCRIPT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts')
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def get_device_id_from_db():
    """Retrieve and return the device_id from the SQLAlchemy database."""
    device = Device.query.first()
    return device.device_id if device else None


def store_response_in_db(response_data):
    """Store the response data in the 'user_info' table using SQLAlchemy."""
    phone_number = f"{response_data['phone_code']}{response_data['phone']}"
    user_info = User(
        user_id=response_data['user_id'],
        name=response_data['name'],
        last_name=response_data['last_name'],
        email=response_data['email'],
        phone_number=phone_number,
        access_token=response_data['access_token']
    )
    try:
        db.session.merge(user_info)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify(f"Error while making the handshake API request: {e}"), 500


def call_handshake_api_and_store_response(device_id):
    """Call the handshake API and store the response in the database."""
    api_url = "https://carfleet.ethansolution.com/api/auth/handshake"
    json_data = {"device_id": device_id}

    try:
        response = requests.post(api_url, json=json_data)
        if response.status_code == 201:
            response_data = response.json()
            if response_data.get("success"):
                store_response_in_db(response_data["data"])
                return jsonify({"message": "Handshake API response stored in the user_info table."}), 201
            else:
                return jsonify(
                    {"message": f"Handshake API response indicates failure: {response_data['message']}"}), 400
        else:
            return jsonify({"message": f"Handshake API request failed: {response.text}"}), 400
    except requests.RequestException as e:
        return jsonify({"message": f"Error while making the handshake API request: {e}"}), 500


@main.route('/')
def index():
    return redirect(url_for('main.device_info'))


@main.route('/device_info')
def device_info():
    return render_template('device_info.html')


@main.route('/setup', methods=['GET'])
def setup():
    if 'logged_in' not in session:
        return redirect(url_for('main.login'))
    scripts = [f for f in os.listdir(SCRIPT_DIR) if os.path.isfile(os.path.join(SCRIPT_DIR, f))]
    return render_template('setup.html', scripts=scripts)


@main.route('/api/devices', methods=['GET'])
def get_devices():
    devices = Device.query.all()
    return jsonify([device.to_dict() for device in devices])


@main.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@main.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] == 'BGSw}:.uDYvCUm<2@#=J$j':  # replace with your password logic
            session['logged_in'] = True
            session.permanent = True
            return redirect(url_for('main.setup'))
        else:
            error = 'Invalid password'
    return render_template('login.html', error=error)


@main.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('main.login'))


@main.route('/create_cron_job', methods=['POST'])
def create_cron_job():
    data = request.json
    script_path = data.get('scriptPath')
    cron_time = data.get('cronTime')

    if not script_path or not os.path.isfile(script_path):
        return jsonify({"message": "Script path is invalid."}), 400

    cron_time_pattern = re.compile(
        r"^(\*|([0-5]?\d)) (\*|([01]?\d|2[0-3])) (\*|([01]?\d|3[01])) (\*|(0?\d|1[0-2])) (\*|([0-6](,\d+)*))$")
    if not cron_time_pattern.match(cron_time):
        return jsonify({"message": "Cron time format is invalid."}), 400

    cron_job = f"{cron_time} /usr/bin/python3 {script_path}"

    try:
        subprocess.run(f"(crontab -l; echo '{cron_job}') | crontab -", shell=True, check=True, executable='/bin/bash')
        return jsonify({"message": "Cron job created successfully."})
    except subprocess.CalledProcessError as e:
        return jsonify({"message": f"Failed to create cron job: {e}"}), 500


@main.route('/video_feed')
def video_feed():
    pass
    # return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# API routes and other functions remain the same

@main.route('/run_script', methods=['POST'])
def run_script():
    data = request.json
    script_name = data.get('script_name')

    if not script_name:
        return jsonify({"error": "No script name provided."}), 400

    script_path = os.path.join(SCRIPT_DIR, script_name)
    if not os.path.isfile(script_path):
        return jsonify({"error": "Script file does not exist."}), 400

    try:
        result = subprocess.run([script_path], capture_output=True, text=True, check=True)
        return jsonify({"output": result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Failed to run script: {e.stderr}"}), 500


@main.route('/change_speed', methods=['POST'])
def change_speed():
    data = request.get_json()
    new_speed = data.get('speed')

    if new_speed is None:
        return jsonify({'error': 'Speed not provided'}), 400

    config_key = 'speed'

    config = Configure.query.filter_by(config_key=config_key).first()
    if config:
        config.config_value = new_speed
        db.session.commit()
    else:
        config = Configure(config_key=config_key, config_value=new_speed)
        db.session.add(config)
        db.session.commit()

    # Restart the facial1.service
    try:
        subprocess.run(["sudo", "systemctl", "restart", "facial1.service"], check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Failed to restart facial1.service', 'details': str(e)}), 500

    return jsonify({'message': 'Speed updated successfully and facial1.service restarted'}), 200


@main.route('/connect_wifi', methods=['POST'])
def connect_wifi():
    data = request.json
    ssid = data.get('ssid')
    password = data.get('password')

    if not ssid or not password:
        logger.error("SSID and password are required.")
        return jsonify({"message": "SSID and password are required."}), 400

    try:
        # Run nmcli command to connect to WiFi
        command = ["sudo", "nmcli", "dev", "wifi", "connect", ssid, "password", password]
        logger.info(f"Running command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        if result.returncode == 0:
            logger.info("WiFi connected successfully.")
            return jsonify({"message": "WiFi connected successfully."})
        else:
            error_message = result.stderr.strip()
            if "no network with SSID" in error_message:
                logger.error("SSID not found.")
                return jsonify({"message": "SSID not found."}), 404
            else:
                logger.error(f"Failed to connect to WiFi: {error_message}")
                return jsonify({"message": f"Failed to connect to WiFi: {error_message}"}), 500
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to connect to WiFi: {e.stderr}")
        return jsonify({"message": f"Failed to connect to WiFi: {e.stderr}"}), 500


@main.route('/create_device', methods=['POST'])
def create_device():
    data = request.json
    device_id = data.get('deviceId')
    # device_type = data.get('deviceType')

    if not device_id:
        return jsonify({"message": "Device id and type are required."}), 400

    try:
        new_device = Device(device_id=device_id)
        db.session.add(new_device)
        db.session.commit()
        return jsonify({"message": "Device created successfully."})
    except Exception as e:
        return jsonify({"message": f"Failed to create device: {e}"}), 500


@main.route('/init_handshake', methods=['POST'])
def init_handshake():
    try:
        device_id = get_device_id_from_db()
        if device_id:
            return call_handshake_api_and_store_response(device_id)
        else:
            return jsonify({"message": "No device_id found in the database"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500
