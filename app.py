from flask import Flask, request, render_template, Response, jsonify
from reader_plate import read_plate
from plate_validator import Plate
import pytesseract
from guards.access_guard import jwt_required, jwt_create
from config.env import secret_key, url_frontend
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
app.secret_key = secret_key
CORS(app, resources={r"/*": {"origins": url_frontend}})
socket = SocketIO(app, cors_allowed_origins= url_frontend)

# Configuración de la ubicación de Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Hp\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
config = '--psm 1'
plate = Plate()

@app.route('/')
def index():
    return jsonify({"404": "Not Found"})

@app.route('/auth', methods=["POST"])
@jwt_required
def auth():
    return jsonify({"access": True})

@app.route('/video_feed')
def video_feed():
    return Response(read_plate(socket), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get-access', methods=["POST"])
def get_access():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    token = jwt_create({
        "username": username
    }, app.secret_key)

    session_data =  {
        "data":{
            "username": username, 
            "roles": []
        }, 
        "token": token}

    data = {"access": True, "info": session_data}
    
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=4000)