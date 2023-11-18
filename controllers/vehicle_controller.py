from flask import jsonify, request
from models.vehicle_model import VehicleModel as vehicle

def found_plate():
    data = request.json
    plate_number = data.get('plate_number')
    
    return jsonify({'access': True, 'info': plate_number})

def get_page_data():
    data = request.json
    print(data)
    per_page = data.get('per_page')
    current_page = data.get('current_page')
    # Si los datos no fueron enviados retornamos un error
    if per_page == None or current_page == None:
        print('hola')
        return jsonify({'error': True, 'message': 'Datos no recibidos'})
    # Si los datos fueron enviados entonces consultamos todos los registros
    found_vehicles = vehicle.load(per_page, current_page)
    # Si el usuario no fue encontrado retornamos un error
    if found_vehicles == None:
        return jsonify({'error': True, 'message': 'Error query'})
    return jsonify({'result': found_vehicles})

def get_vehicles_types():
    types = vehicle.get_vehicle_types()
    return jsonify({'result':types})

def get_access_types():
    types = vehicle.get_access_types()
    return jsonify({'result':types})

def get_status_types():
    types = vehicle.get_status_types()
    return jsonify({'result':types})

def get_total_rows():
    counted = vehicle.get_total()
    return jsonify({'result':counted})
    