import jwt
from functools import wraps
from flask import request, jsonify, current_app

# Middleware de autenticación JWT
def jwt_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'auth': False, 'error': 'Token not received'}), 401

        try:
            # Decodificar el token y verificar la firma con la clave secreta
            token = token.split(" ")
            print(token)
            if len(token) == 2: 
                token = token[1]
            data = jwt.decode(token, current_app.secret_key, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'auth': False, 'error': 'Secret key invalid'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'auth': False, 'error': 'Token de autenticación inválido'}), 401

        # El usuario está autenticado, puedes acceder a 'data' para obtener más información
        return func(*args, **kwargs)

    return decorated

def jwt_create(payload, secret_key):
     return jwt.encode(payload, secret_key, algorithm='HS256')


