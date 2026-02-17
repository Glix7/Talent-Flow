"""
API endpoints for Employee management.
"""
from flask import jsonify, request, abort
from . import blueprint
from app.services.employee_service import EmployeeService

@blueprint.route('/api/employees', methods=['GET'])
def get_employees():
    """
    Get all employees list.
    """
    employees = EmployeeService.get_all_employees()
    return jsonify([emp.to_dict() for emp in employees])

@blueprint.route('/api/employees/<int:id>', methods=['GET'])
def get_employee(id):
    """
    Get single employee details.
    """
    employee = EmployeeService.get_employee_by_id(id)
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404
    return jsonify(employee.to_dict())

@blueprint.route('/api/employees', methods=['POST'])
def create_employee():
    """
    Create a new employee.
    """
    data = request.get_json()
    if not data or not 'name' in data or not 'email' in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        new_emp = EmployeeService.create_employee(data)
        return jsonify(new_emp.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500
