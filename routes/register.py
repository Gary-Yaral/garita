from flask import Blueprint
from controllers import register_controller
from guards.access_guard import jwt_required

register_bp = Blueprint('register', __name__, url_prefix='/register')

@register_bp.route('/load', methods=['POST'])
@jwt_required
def load():
  return register_controller.get_page_data()

@register_bp.route('/filter', methods=['POST'])
@jwt_required
def filter_data():
  return register_controller.get_filtered_data()

@register_bp.route('/total', methods=['POST'])
@jwt_required
def totalRows():
  return register_controller.get_total_rows()

@register_bp.route('/types', methods=['GET'])
@jwt_required
def get_driver_types():
  return register_controller.get_types()

@register_bp.route('/new', methods=['POST'])
@jwt_required
def add_drive():
  return register_controller.add()

@register_bp.route('/update', methods=['POST'])
@jwt_required
def update_drive():
  return register_controller.update()

@register_bp.route('/delete', methods=['POST'])
@jwt_required
def delete_drive():
  return register_controller.delete()

@register_bp.route('/home-arrival-data', methods=['GET'])
@jwt_required
def get_home_arrival_data():
  return register_controller.get_home_arrival_data()

@register_bp.route('/home-exit-data', methods=['GET'])
@jwt_required
def get_home_exit_data():
  return register_controller.get_home_exit_data()

    
        

