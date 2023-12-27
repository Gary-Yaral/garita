from flask import Flask, jsonify
import pytesseract
from config.env import secret_key,url_frontend
from flask_cors import CORS
from routes import user, driver, vehicle, excel, register

app = Flask(__name__)

app.secret_key = secret_key
CORS(app, resources={r"/*": {"origins": url_frontend}}, expose_headers=["Content-Disposition"])

# Configuración de la ubicación de Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Hp\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
config = '--psm 1'

app.register_blueprint(user.user_bp, url_prefix='/user')
app.register_blueprint(driver.driver_bp, url_prefix='/driver')
app.register_blueprint(vehicle.vehicle_bp, url_prefix='/vehicle')
app.register_blueprint(register.register_bp, url_prefix='/register')
app.register_blueprint(excel.excel_bp, url_prefix='/excel')

# Si hacen peticion a ruta no establecida
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"404": "Not Found"})


if __name__ == "__main__":
    app.run(debug=True, port=5800)