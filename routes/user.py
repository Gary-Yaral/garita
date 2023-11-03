from flask import Blueprint
from controllers.user_controller import login_user

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/get-access', methods=["POST"])
def access():
    return login_user()

    
        

