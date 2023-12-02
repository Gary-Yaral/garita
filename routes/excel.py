
from flask import Blueprint
from controllers import excel_controller

excel_bp = Blueprint('excel', __name__, url_prefix='/excel')

@excel_bp.route('/create', methods=['POST']) 
def generate_excel():
    return excel_controller.generate_excel()