from flask import jsonify, request
from models.register_model import RegisterModel as registers

def get_page_data():
    data = request.json
    per_page = data.get('per_page')
    current_page = data.get('current_page')
    # Si los datos no fueron enviados retornamos un error
    if per_page == None or current_page == None:
        return jsonify({'error': True, 'message': 'Datos no recibidos'})
    # Si los datos fueron enviados entonces consultamos todos los registros
    found_registers = registers.load(per_page, current_page)
    # Si el usuario no fue encontrado retornamos un error
    if found_registers == None:
        return jsonify({'error': True, 'message': 'Error query'})
    return jsonify({'result': found_registers})

def get_filtered_data():
    data = request.json
    per_page = data.get('per_page')
    current_page = data.get('current_page')
    filter_text = data.get('filter')
    # Si los datos no fueron enviados retornamos un error
    if per_page == None or current_page == None or filter_text == None:
        return jsonify({'error': True, 'message': 'Datos no recibidos'})
    # Si los datos fueron enviados entonces filtramos los datos
    found_registers = registers.filter(per_page, current_page, filter_text)
    # Si el usuario no fue encontrado retornamos un error
    if found_registers == None:
        return jsonify({'error': True, 'message': 'Error query'})
    return jsonify({'result': found_registers})

def get_total_rows():
    counted = registers.get_total()
    return jsonify({'result':counted})

def get_types():
    types = registers.get_types()
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
    result = registers.update(_id, dni, name, surname, type_id)
    return jsonify({'result':result})

def add():
    data = request.json
    dni = data.get('dni')
    name = data.get('name')
    surname = data.get('surname')
    type_id = data.get('type_id')
    if dni == None or name == None or surname == None or type_id == None:
        return jsonify({'error': True, 'message': 'Datos no recibidos'})
    result = registers.addNew(dni, name, surname, type_id)
    return jsonify({'result':result})

def delete():
    data = request.json
    _id = data.get('id')
    if _id == None:
        return jsonify({'error': True, 'message': 'Datos no recibidos'})
    result = registers.delete(_id)
    return jsonify({'result':result})