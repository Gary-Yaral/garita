from flask import Blueprint
from controllers import user_controller

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/get-access', methods=["POST"])
def access():
    return user_controller.login_user()

@user_bp.route('/load', methods=["POST"])
def load():
    return user_controller.get_page_data()

    
        

