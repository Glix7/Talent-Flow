"""
Service layer for Employee operations.
"""
from app.extensions import db
from app.models.employee import Employee
from app.models.attendance import Attendance
from sqlalchemy.exc import IntegrityError
from datetime import datetime


class EmployeeService:
    @staticmethod
    def create_employee(data):
        """
        Create a new employee.
        """
        try:
            # Basic validation
            date_str = data.get('date_of_joining')
            doj = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.utcnow().date()

            new_emp = Employee(
                name=data['name'],
                email=data['email'],
                phone=data.get('phone'),
                address=data.get('address'),
                designation=data['designation'],
                department=data['department'],
                date_of_joining=doj
            )
            db.session.add(new_emp)
            db.session.commit()
            return new_emp
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Email already exists")
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_employees(department=None):
        """
        Retrieve all employees, optionally filtered by department.
        """
        query = Employee.query
        if department:
            query = query.filter_by(department=department)
        return query.all()


    @staticmethod
    def get_employee_by_id(emp_id):
        """
        Retrieve a single employee by ID.
        """
        return Employee.query.get(emp_id)

    @staticmethod
    def update_employee(emp_id, data):
        """
        Update employee details.
        """
        employee = Employee.query.get(emp_id)
        if not employee:
            return None
        
        if 'name' in data: employee.name = data['name']
        if 'email' in data: employee.email = data['email']
        if 'phone' in data: employee.phone = data['phone']
        if 'address' in data: employee.address = data['address']
        if 'designation' in data: employee.designation = data['designation']
        if 'department' in data: employee.department = data['department']
        
        try:
            db.session.commit()
            return employee
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Email already exists")

    @staticmethod
    def delete_employee(emp_id):
        """
        Delete an employee and their associated attendance records.
        """
        employee = Employee.query.get(emp_id)
        if not employee:
            return False
            
        # Manually delete attendance records first
        Attendance.query.filter_by(employee_id=emp_id).delete()
        
        db.session.delete(employee)
        db.session.commit()
        return True





