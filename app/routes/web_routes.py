"""
Web routes for serving HTML pages.
"""
from flask import render_template
from . import blueprint
from app.services.employee_service import EmployeeService
from app.services.attendance_service import AttendanceService
from app.extensions import db
from app.models.employee import Employee
from sqlalchemy import func

@blueprint.route('/')
def index():
    """
    Home page: Lists all employees.
    Supports filtering by department ?department=XY
    """
    dept_filter = request.args.get('department')
    employees = EmployeeService.get_all_employees(department=dept_filter)
    
    # Get all unique departments for the dropdown filter
    # Ideally this belongs in a service, doing it inline for simplicity
    all_depts = db.session.query(Employee.department).distinct().all()
    departments = [d[0] for d in all_depts]
    
    return render_template('home.html', employees=employees, departments=departments, current_filter=dept_filter)


@blueprint.route('/employee/<int:id>')
def employee_detail(id):
    """
    Employee Detail Page: Shows info + attendance.
    """
    employee = EmployeeService.get_employee_by_id(id)
    if not employee:
        return render_template('404.html'), 404
        
    attendance = AttendanceService.get_attendance_history(id)
    from datetime import datetime
    today_date = datetime.now().date()
    return render_template('employee_detail.html', employee=employee, attendance=attendance, today_date=today_date)


@blueprint.route('/reports')
def reports_page():
    """
    Reports Page: Visualizes department data.
    """
    results = db.session.query(Employee.department, func.count(Employee.id))\
        .group_by(Employee.department).all()
    
    labels = [r[0] for r in results]
    data = [r[1] for r in results]
    
    return render_template('reports.html', labels=labels, data=data)

from flask import request, redirect, url_for

@blueprint.route('/employees/new', methods=['GET', 'POST'])
def new_employee():
    """
    Create a new employee via HTML form.
    """
    if request.method == 'POST':
        data = request.form.to_dict()
        try:
            EmployeeService.create_employee(data)
            return redirect(url_for('main.index'))
        except ValueError as e:
            return render_template('add_employee.html', error=str(e))
    
    return render_template('add_employee.html')

@blueprint.route('/attendance/mark/<int:emp_id>', methods=['POST'])
def mark_attendance_web(emp_id):
    """
    Mark attendance via Web UI with strict logic:
    1. If no record for today -> Mark IN.
    2. If record exists and OUT is null -> Mark OUT.
    3. If record exists and OUT is set -> Do nothing (or flash message).
    """
    from datetime import datetime
    now = datetime.now()
    today_str = now.strftime('%Y-%m-%d')
    
    # Get history to check for today's record
    current_record = AttendanceService.get_attendance_history(emp_id)
    today_record = next((r for r in current_record if str(r.date) == today_str), None)
    
    data = {
        'employee_id': emp_id,
        'date': today_str
    }

    if not today_record:
        # Case 1: New Record -> IN TIME
        data['in_time'] = now.strftime('%H:%M')
        AttendanceService.mark_attendance(data)
        
    elif today_record.in_time and not today_record.out_time:
        # Case 2: Punching OUT
        data['out_time'] = now.strftime('%H:%M')
        AttendanceService.mark_attendance(data)
        
    else:
        # Case 3: Already done for the day
        # Ideally we would flash a message here, but for now we just don't update anything
        pass
    
    return redirect(url_for('main.employee_detail', id=emp_id))


@blueprint.route('/employees/<int:id>/edit', methods=['GET', 'POST'])
def edit_employee(id):
    """
    Edit Employee Details.
    """
    employee = EmployeeService.get_employee_by_id(id)
    if not employee:
        return render_template('404.html'), 404

    if request.method == 'POST':
        data = request.form.to_dict()
        try:
            EmployeeService.update_employee(id, data)
            return redirect(url_for('main.employee_detail', id=id))
        except ValueError as e:
            return render_template('edit_employee.html', employee=employee, error=str(e))

    return render_template('edit_employee.html', employee=employee)

@blueprint.route('/attendance/<int:att_id>/edit', methods=['GET', 'POST'])
def edit_attendance(att_id):
    """
    Manually update an attendance record.
    """
    record = AttendanceService.get_attendance_by_id(att_id)
    if not record:
        return render_template('404.html'), 404
        
    if request.method == 'POST':
        data = request.form.to_dict()
        AttendanceService.update_attendance(att_id, data)
        return redirect(url_for('main.employee_detail', id=record.employee_id))
        
    return render_template('edit_attendance.html', record=record)

@blueprint.route('/employees/<int:id>/delete', methods=['POST'])
def delete_employee(id):
    """
    Delete an employee.
    """
    success = EmployeeService.delete_employee(id)
    if not success:
        return render_template('404.html'), 404
    return redirect(url_for('main.index'))


@blueprint.route('/api')
def api_docs():
    """
    Serve API Documentation page.
    """
    return render_template('api_docs.html')







