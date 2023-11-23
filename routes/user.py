from flask import Blueprint
from controllers import user_controller

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/get-access', methods=["POST"])
def access():
    return user_controller.login_user()

@user_bp.route('/load', methods=["POST"])
def load():
    return user_controller.get_page_data()

@user_bp.route('/new', methods=["POST"])
def add_user():
    return user_controller.add()
@user_bp.route('/update', methods=["POST"])
def update_user():
    return user_controller.update()

@user_bp.route('/delete', methods=["POST"])
def delete_user():
    return user_controller.delete()

@user_bp.route('/total', methods=["POST", "GET"])
def total_rows():
    return user_controller.get_total_rows()

@user_bp.route('/types', methods=["POST", "GET"])
def load_types():
    return user_controller.get_status_types()

@user_bp.route('/filter', methods=["POST", "GET"])
def filter_data():
    return user_controller.get_filtered_data()

@user_bp.route('/roles', methods=["POST", "GET"])
def get_roles():
    return user_controller.get_roles()


    
        

