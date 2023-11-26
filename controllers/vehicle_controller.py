from flask import jsonify, request
from models.vehicle_model import VehicleModel as vehicle

# Permite a la cámara buscar la placa detectada 
def found_plate():
    data = request.json
    plate_number = data.get('plate_number')
    
    return jsonify({'access': True, 'info': plate_number})

# Hace el filtrado segun un dato en enviaodo
def get_filtered_data():
    data = request.json
    per_page = data.get('per_page')
    current_page = data.get('current_page')
    filter_text = data.get('filter')
    # Si los datos no fueron enviados retornamos un error
    if per_page == None or current_page == None or filter_text == None:
        return jsonify({'error': True, 'message': 'Datos no recibidos'})
    # Si los datos fueron enviados entonces filtramos los datos
    found_data = vehicle.filter(per_page, current_page, filter_text)
    # Si el usuario no fue encontrado retornamos un error
    if found_data == None:
        return jsonify({'error': True, 'message': 'Error query'})
    return jsonify({'result': found_data})

# Carga los datos de la página actual de la tabla
def get_page_data():
    data = request.json
    per_page = data.get('per_page')
    current_page = data.get('current_page')
    # Si los datos no fueron enviados retornamos un error
    if per_page == None or current_page == None:
        return jsonify({'error': True, 'message': 'Datos no recibidos'})
    # Si los datos fueron enviados entonces consultamos todos los registros
    found_vehicles = vehicle.load(per_page, current_page)
    # Si el usuario no fue encontrado retornamos un error
    if found_vehicles == None:
        return jsonify({'error': True, 'message': 'Error query'})
    return jsonify({'result': found_vehicles})

# Funciones que cargan los datos del formulario 
def get_vehicles_types():
    types = vehicle.get_vehicle_types()
    return jsonify({'result':types})

def get_access_types():
    types = vehicle.get_access_types()
    return jsonify({'result':types})

def get_status_types():
    types = vehicle.get_status_types()
    return jsonify({'result':types})

def get_formdata_required():
    data = vehicle.load_required_data()
    return jsonify({'result':data})

def get_total_rows():
    counted = vehicle.get_total()
    return jsonify({'result':counted})

# Funciones CRUD
def add():
    data = request.json
    plate_number = data.get('plate_number') 
    access_type_id = data.get('access_type_id') 
    vehicle_type_id = data.get('vehicle_type_id') 
    status_type_id = data.get('status_type_id')
    if plate_number == None or access_type_id == None or vehicle_type_id == None or status_type_id == None:
        return jsonify({'error': True, 'message': 'Datos no recibidos'})
    result = vehicle.addNew(plate_number, access_type_id, vehicle_type_id, status_type_id)
    return jsonify({'result':result})

def update():
    data = request.json
    print(data)
    _id = data.get('id')
    plate_number = data.get('plate_number') 
    access_type_id = data.get('access_type_id') 
    vehicle_type_id = data.get('vehicle_type_id') 
    status_type_id = data.get('status_type_id')
    if _id == None or plate_number == None or access_type_id == None or vehicle_type_id == None or status_type_id == None:
        return jsonify({'error': True, 'message': 'Datos no recibidos'})
    result = vehicle.update(_id, plate_number, access_type_id, vehicle_type_id, status_type_id)
    return jsonify({'result':result})

def delete():
    data = request.json
    _id = data.get('id')
    if _id == None:
        return jsonify({'error': True, 'message': 'Datos no recibidos'})
    result = vehicle.delete(_id)
    return jsonify({'result':result}) 

