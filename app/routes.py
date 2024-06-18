import os
import re
import subprocess

import cv2
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify

from app.models import Device, User

main = Blueprint('main', __name__)

SCRIPT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts')


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

    cron_job = f"{cron_time} {script_path}"

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
