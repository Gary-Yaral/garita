from flask import Blueprint
from controllers.driver_controller import get_page_data, get_total_rows
from guards.access_guard import jwt_required

driver_bp = Blueprint('driver', __name__, url_prefix='/driver')

@driver_bp.route('/load', methods=['POST'])
@jwt_required
def load():
  return get_page_data()

@driver_bp.route('/total', methods=['POST'])
@jwt_required
def totalRows():
  return get_total_rows()

    
        

