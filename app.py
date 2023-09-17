from flask import Flask, render_template, Response
import pytesseract
from reader_plate import read_plate
from plate_validator import Plate
from utils import data

app = Flask(__name__)

# Configuración de la ubicación de Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Hp\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
config = '--psm 1'
plate = Plate()

@app.route('/')
def index():
    return render_template('index.html', data=data)

@app.route('/camera')
def video_camera():
    return render_template('camera.html', data=data)

@app.route('/video_feed')
def video_feed():
    return Response(read_plate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True, port=4000)