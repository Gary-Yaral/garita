from flask import Flask, jsonify, g
import pytesseract
from config.env import secret_key, url_frontend
from flask_cors import CORS
from routes import user, driver, vehicle
from db_config.mysql import MysqlDB

app = Flask(__name__)

app.secret_key = secret_key
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuración de la ubicación de Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Hp\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
config = '--psm 1'

app.register_blueprint(user.user_bp, url_prefix='/user')
app.register_blueprint(driver.driver_bp, url_prefix='/driver')
app.register_blueprint(vehicle.vehicle_bp, url_prefix='/vehicle')

@app.teardown_appcontext
def close_db_connection(exception=None):
    if exception:
        print(f"An exception occurred: {exception}")

    mysql_db = MysqlDB()  # Crea una instancia de tu clase MysqlDB
    mysql_db.close_connection()  # Cierra todas las conexiones al finalizar la aplicación

# Si hacen peticion a ruta no establecida
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"404": "Not Found"})


if __name__ == "__main__":
    app.run(debug=True, port=5800)