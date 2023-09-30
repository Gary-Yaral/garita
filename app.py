from flask import Flask, Response, jsonify
from reader_plate import read_plate
from plate_validator import Plate
import pytesseract
from guards.access_guard import jwt_required
from config.env import secret_key, url_frontend
from flask_cors import CORS
from flask_socketio import SocketIO
from routes import user

app = Flask(__name__)
app.secret_key = secret_key
CORS(app, resources={r"/*": {"origins": url_frontend}})
socket = SocketIO(app, cors_allowed_origins= url_frontend)

# Configuración de la ubicación de Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Hp\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
config = '--psm 1'
plate = Plate()

app.register_blueprint(user.user_bp)

@app.route('/auth', methods=["POST"])
@jwt_required
def auth():
    return jsonify({"access": True})

@app.route('/video_feed')
def video_feed():
    return Response(read_plate(socket), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"404": "Not Found"})


if __name__ == "__main__":
    app.run(debug=True, port=4000)