from flask import current_app, jsonify, request
from guards.access_guard import jwt_create
from models.driver_model import DriverModel as drivers

def get_page_data():
    data = request.json
    per_page = data.get('per_page')
    current_page = data.get('current_page')
    # Si los datos no fueron enviados retornamos un error
    if per_page == None and current_page == None:
        return jsonify({'error': True, 'message': 'Datos no recibidos'})
    # Si los datos fueron enviados entonces buscamos el usuario
    found_drivers = drivers.load(per_page, current_page)
    # Si el usuario no fue encontrado retornamos un error
    if found_drivers == None:
        return jsonify({'error': True, 'message': 'Error query'})
    return jsonify({'drivers': found_drivers})

def get_total_rows():
    counted = drivers.get_total()
    return jsonify({'drivers':counted})