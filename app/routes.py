import os
import re
import subprocess
import cv2
from flask import Blueprint, render_template, request, jsonify, Response

from app.models import Device, User

main = Blueprint('main', __name__)

# Define the directory containing your scripts
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
    scripts = [f for f in os.listdir(SCRIPT_DIR) if os.path.isfile(os.path.join(SCRIPT_DIR, f))]
    return render_template('index.html', scripts=scripts)


@main.route('/api/devices', methods=['GET'])
def get_devices():
    devices = Device.query.all()
    return jsonify([device.to_dict() for device in devices])


@main.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@main.route('/run_script', methods=['POST'])
def run_script():
    script_name = request.json.get('script_name')
    if not script_name or not os.path.isfile(os.path.join(SCRIPT_DIR, script_name)):
        return jsonify({"error": "Script not found"}), 404

    script_path = os.path.join(SCRIPT_DIR, script_name)
    result = subprocess.run([script_path], capture_output=True, text=True, shell=True)

    combined_result = {
        "output": result.stdout + "\n" + result.stderr
    }

    return jsonify(combined_result)


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
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
