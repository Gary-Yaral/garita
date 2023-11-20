from flask import current_app, jsonify, request
from guards.access_guard import jwt_create
from models.user_model import UserSystem as user
from db_constants.global_constants import UserStatus, UserRoles
from pwd_md.pass_config import verify_password

user_status = UserStatus()
user_roles = UserRoles()

def login_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    # Si los datos no fueron enviados retornamos un error
    if username == None and password == None:
        return jsonify({'error': True, 'message': 'Datos no recibidos'})
    # Si los datos fueron enviados entonces buscamos el usuario
    found_user = user.find_user(username)
    # Si el usuario no fue encontrado retornamos un error
    if found_user == None:
        return jsonify({'error': True, 'message': 'Usuario o contraseña incorrectos'})
    # Si las contraseñas no son las mismas retornamos un error
    if verify_password(password, found_user['password']) == False: 
        return jsonify({'error': True, 'message': 'Usuario o contraseña incorrectos'})
    # Si el usuario está deshabilitado devolvemos un error
    status = user.find_user_status(found_user['fk_user_status_id'])
    if status == user_status.DISABLED: 
        return jsonify({'error': True, 'message': 'Usuario deshabilitado, comuniquese con el administrador'})
    # Obtenemos todos los roles que tiene ese usuario
    roles = user.get_user_roles(found_user['id'])
    # Verificamos si es admin y puede agregar otros usuarios
    isAdmin = False
    isSuper = False
    for rol in roles: 
        if bool(rol['editor']):
            isAdmin = True
        if rol['rol_name'] == user_roles.SUPER:
            isSuper = True

    # Eliminamos datos privados antes de crear el token
    del found_user['username']
    del found_user['password']
    del found_user['fk_user_status_id']
    # Generamos el token que se usará para las peticiones
    token = jwt_create({
        'data': {
            'user': found_user,
            'roles': roles
        }
    }, current_app.secret_key)
    # Creamos la sesion que devolveremos
    session_data =  {
        'data':{
            'user':found_user,
            'roles': None 
        },
        'token': token}
    # Si es super usuario añadimos rol de super y admin y retornamos
    if isSuper: 
        session_data['data']['user']['dni'] = "xxxxxxxxxx"
        session_data['data']['roles'] = (user_roles.SUPER, user_roles.ADMINISTRADOR, user_roles.USER)
        return jsonify({'access': True, 'info': session_data})
    
    # Si es admin tendrá rol admin y retornará
    if isAdmin: 
        session_data['data']['roles'] = (user_roles.ADMINISTRADOR, user_roles.USER)
        return jsonify({'access': True, 'info': session_data})
    # Si no es super ni admin entonces tendrá rol de usuario
    session_data['data']['roles'] = (user_roles.USER,)
    return jsonify({'access': True, 'info': session_data})

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
    found_data = user.filter(per_page, current_page, filter_text)
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
    found_vehicles = user.load(per_page, current_page)
    # Si el usuario no fue encontrado retornamos un error
    if found_vehicles == None:
        return jsonify({'error': True, 'message': 'Error query'})
    return jsonify({'result': found_vehicles})

# Funciones que cargan los datos del formulario 
def get_status_types():
    types = user.get_status_types()
    return jsonify({'result':types})

def get_total_rows():
    counted = user.get_total()
    return jsonify({'result':counted})


# Funciones CRUD
def add():
    data = request.json
    dni = data.get('dni') 
    name = data.get('name') 
    surname = data.get('surname') 
    username = data.get('username') 
    password = data.get('password') 
    user_status_id = data.get('user_status_id')
    if dni == None or name == None or username == None or surname == None or password == None or user_status_id == None:
        return jsonify({'error': True, 'message': 'Datos no recibidos'})
    result = user.addNew(dni, name, surname, username, password, user_status_id)
    return jsonify({'result':result})

def update():
    data = request.json
    _id = data.get('id')
    dni = data.get('dni') 
    name = data.get('name') 
    surname = data.get('surname') 
    username = data.get('username') 
    password = data.get('password') 
    user_status_id = data.get('user_status_id')
    print(password)
    if _id == None or dni == None or name == None or username == None or surname == None or password == None or user_status_id == None:
        return jsonify({'error': True, 'message': 'Datos no recibidos'})
    result = user.update(_id, dni, name, surname, username, password, user_status_id)
    return jsonify({'result':result})



def delete():
    data = request.json
    _id = data.get('id')
    if _id == None:
        return jsonify({'error': True, 'message': 'Datos no recibidos'})
    result = user.delete(_id)
    return jsonify({'result':result}) 