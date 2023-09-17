from flask import Flask, render_template, Response, jsonify
from reader_plate import read_plate
from plate_validator import Plate
from utils import data, system_name
import pytesseract
from validate_access import access

app = Flask(__name__)

# Configuración de la ubicación de Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Hp\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
config = '--psm 1'
plate = Plate()

@app.route('/')
def index():
    return render_template('index.html', data=data, system_name=system_name)

@app.route('/get-access', methods=["POST"])
def get_access():
    return jsonify(access.login())

@app.route('/camera')
def video_camera():
    return render_template('camera.html', data=data)

@app.route('/access')
def access_page():
    return render_template('access.html', system_name=system_name)

@app.route('/video_feed')
def video_feed():
    return Response(read_plate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True, port=4000)