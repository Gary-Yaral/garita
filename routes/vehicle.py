from flask import Blueprint
from controllers import vehicle_controller
from guards.access_guard import jwt_required

vehicle_bp = Blueprint('vehicle', __name__, url_prefix='/vehicle')

@vehicle_bp.route('/load', methods=['POST'])
@jwt_required
def load():
  return vehicle_controller.get_page_data()

@vehicle_bp.route('/types', methods=['GET'])
@jwt_required
def get_vehicle_types():
  return vehicle_controller.get_vehicles_types()

@vehicle_bp.route('/access-types', methods=['GET'])
@jwt_required
def get_access_types():
  return vehicle_controller.get_access_types()

@vehicle_bp.route('/status-types', methods=['GET'])
@jwt_required
def get_status_types():
  return vehicle_controller.get_status_types()

@vehicle_bp.route('/total', methods=['POST'])
@jwt_required
def total_rows():
  return vehicle_controller.get_total_rows()

@vehicle_bp.route('/new', methods=['POST'])
@jwt_required
def add_drive():
  return vehicle_controller.add()

@vehicle_bp.route('/update', methods=['POST'])
@jwt_required
def update_drive():
  return vehicle_controller.update()

@vehicle_bp.route('/delete', methods=['POST'])
@jwt_required
def delete_drive():
  return vehicle_controller.delete()

@vehicle_bp.route('/filter', methods=['POST'])
@jwt_required
def filter_data():
  return vehicle_controller.get_filtered_data() 

@vehicle_bp.route('/data-form', methods=['GET'])
@jwt_required
def required_data():
  return vehicle_controller.get_formdata_required() 