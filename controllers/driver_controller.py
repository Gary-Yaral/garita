from flask import jsonify, request
from models.driver_model import DriverModel as drivers

def get_page_data():
    data = request.json
    per_page = data.get('per_page')
    current_page = data.get('current_page')
    # Si los datos no fueron enviados retornamos un error
    if per_page == None or current_page == None:
        return jsonify({'error': True, 'message': 'Datos no recibidos'})
    # Si los datos fueron enviados entonces consultamos todos los registros
    found_drivers = drivers.load(per_page, current_page)
    # Si el usuario no fue encontrado retornamos un error
    if found_drivers == None:
        return jsonify({'error': True, 'message': 'Error query'})
    return jsonify({'result': found_drivers})

def get_filtered_data():
    data = request.json
    per_page = data.get('per_page')
    current_page = data.get('current_page')
    filter_text = data.get('filter')
    # Si los datos no fueron enviados retornamos un error
    if per_page == None or current_page == None or filter_text == None:
        return jsonify({'error': True, 'message': 'Datos no recibidos'})
    # Si los datos fueron enviados entonces filtramos los datos
    found_drivers = drivers.filter(per_page, current_page, filter_text)
    # Si el usuario no fue encontrado retornamos un error
    if found_drivers == None:
        return jsonify({'error': True, 'message': 'Error query'})
    return jsonify({'result': found_drivers})

def get_total_rows():
    counted = drivers.get_total()
    return jsonify({'result':counted})

def get_types():
    types = drivers.get_types()
    return jsonify({'result':types})

def update():
    data = request.json
    _id = data.get('id')
    dni = data.get('dni')
    name = data.get('name')
    surname = data.get('surname')
    type_id = data.get('type_id')
    if _id == None or dni == None or name == None or surname == None or type_id == None:
        return jsonify({'error': True, 'message': 'Datos no recibidos'})
    result = drivers.update(_id, dni, name, surname, type_id)
    return jsonify({'result':result})

def add():
    data = request.json
    dni = data.get('dni')
    name = data.get('name')
    surname = data.get('surname')
    type_id = data.get('type_id')
    if dni == None or name == None or surname == None or type_id == None:
        return jsonify({'error': True, 'message': 'Datos no recibidos'})
    result = drivers.addNew(dni, name, surname, type_id)
    return jsonify({'result':result})

def delete():
    data = request.json
    _id = data.get('id')
    if _id == None:
        return jsonify({'error': True, 'message': 'Datos no recibidos'})
    result = drivers.delete(_id)
    return jsonify({'result':result})

def find_driver():
    data = request.json
    dni = data.get('dni')
    if not dni:
        return jsonify({'error': True, 'message': 'Datos no recibidos'})
    result = drivers.find_driver(dni)
    return jsonify({'result':result})