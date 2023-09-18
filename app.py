from flask import Flask, request, render_template, Response, jsonify
from reader_plate import read_plate
from plate_validator import Plate
from utils import data, system_name
import pytesseract
from validate_access import access
from guards.access_guard import jwt_required, jwt_create
from config.env import secret_key
import requests

app = Flask(__name__)
app.secret_key = secret_key
app.config['SESSION_COOKIE_NAME'] = secret_key


# Configuración de la ubicación de Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Hp\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
config = '--psm 1'
plate = Plate()

@app.route('/')
def index():
    return render_template('access.html', system_name=system_name)


@app.route('/home', methods=["GET"])
def home_page():
    return render_template('index.html', data=data, system_name=system_name)

@app.route('/auth', methods=["POST"])
@jwt_required
def auth():
    return jsonify({"access": True})

@app.route('/camera')
def video_camera():
    return render_template('camera.html', data=data)

@app.route('/access')
def access_page():
    return render_template('access.html', system_name=system_name)

@app.route('/video_feed')
def video_feed():
    return Response(read_plate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get-access', methods=["POST"])
def get_access():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    token = jwt_create({
        "username": username
    }, app.secret_key),

    data = {"access": True, "token": token[0]}
    
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=4000)