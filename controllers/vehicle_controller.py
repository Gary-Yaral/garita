from flask import current_app, jsonify, request
from models.user_model import UserSystem as user
from db_constants.global_constants import UserStatus, UserRoles
from pwd_md.pass_config import verify_password

user_status = UserStatus()
user_roles = UserRoles()

def found_plate():
    data = request.json
    plate_number = data.get('plate_number')
    
    return jsonify({'access': True, 'info': plate_number})
    