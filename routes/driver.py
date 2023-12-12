from flask import Blueprint
from controllers import driver_controller as controller
from guards.access_guard import jwt_required

driver_bp = Blueprint('driver', __name__, url_prefix='/driver')

@driver_bp.route('/load', methods=['POST'])
@jwt_required
def load():
  return controller.get_page_data()

@driver_bp.route('/filter', methods=['POST'])
@jwt_required
def filter_data():
  return controller.get_filtered_data()

@driver_bp.route('/total', methods=['POST'])
@jwt_required
def totalRows():
  return controller.get_total_rows()

@driver_bp.route('/types', methods=['GET'])
@jwt_required
def get_driver_types():
  return controller.get_types()

@driver_bp.route('/new', methods=['POST'])
@jwt_required
def add_drive():
  return controller.add()

@driver_bp.route('/update', methods=['POST'])
@jwt_required
def update_drive():
  return controller.update()

@driver_bp.route('/delete', methods=['POST'])
@jwt_required
def delete_drive():
  return controller.delete()

@driver_bp.route('/find', methods=['POST'])
@jwt_required
def find_driver():
  return controller.find_driver()

    
        

