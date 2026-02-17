from flask import Blueprint

blueprint = Blueprint('main', __name__)

from . import api_employee, api_attendance, web_routes, report_routes
