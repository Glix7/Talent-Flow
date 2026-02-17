"""
Routes for reporting.
"""
from flask import jsonify, render_template
from . import blueprint
from app.extensions import db
from app.models.employee import Employee
from sqlalchemy import func

@blueprint.route('/report/departments', methods=['GET'])
def department_report():
    """
    Return JSON report of count of employees per department.
    And renders a simple chart view if requested via browser.
    """
    # Query: SELECT department, COUNT(id) FROM employees GROUP BY department
    results = db.session.query(Employee.department, func.count(Employee.id))\
        .group_by(Employee.department).all()
    
    data = {dept: count for dept, count in results}
    
    # If the client accepts HTML, render a template (optional requirement but good UI)
    # For now, just JSON as per primary API requirement, but the user asked for a route too
    # We will support a UI view in web_routes, this API endpoint returns data.
    return jsonify(data)
