"""
Service layer for Attendance operations.
"""
from app.extensions import db
from app.models.attendance import Attendance
from app.models.employee import Employee
from datetime import datetime

class AttendanceService:
    @staticmethod
    def mark_attendance(data):
        """
        Mark attendance for an employee.
        Expects: employee_id, date (optional), in_time (optional), out_time (optional)
        """
        emp_id = data.get('employee_id')
        employee = Employee.query.get(emp_id)
        if not employee:
            raise ValueError("Employee not found")

        date_str = data.get('date')
        if date_str:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            date_obj = datetime.utcnow().date()

        # Check if record exists for this day
        attendance = Attendance.query.filter_by(employee_id=emp_id, date=date_obj).first()
        
        if not attendance:
            attendance = Attendance(employee_id=emp_id, date=date_obj)
            db.session.add(attendance)

        # Update times if provided (and not overwrite existing unless explicitly nullifying which isn't the case here)
        if 'in_time' in data and data['in_time']:
             # Only set IN time if it's a new record or we are explicitly forcing it (API/Edit). 
             # For the basic flow, we trust the caller (route) to send the right data.
             # However, to be safe: don't overwrite if it exists and we assume this might be a mistake? 
             # Actually, the route logic handles the 'logic', service just does what it's told.
             # But let's respect that if the record exists, we update fields.
             attendance.in_time = datetime.strptime(data['in_time'], '%H:%M').time()
        
        if 'out_time' in data and data['out_time']:
            attendance.out_time = datetime.strptime(data['out_time'], '%H:%M').time()

        db.session.commit()

        return attendance

    @staticmethod
    def get_attendance_history(emp_id):
        """
        Get attendance records for a specific employee.
        """
        return Attendance.query.filter_by(employee_id=emp_id).order_by(Attendance.date.desc()).all()

    @staticmethod
    def get_attendance_by_id(att_id):
        return Attendance.query.get(att_id)

    @staticmethod
    def update_attendance(att_id, data):
        """
        Update a specific attendance record (e.g. correct times).
        """
        record = Attendance.query.get(att_id)
        if not record:
            return None
            
        if 'in_time' in data and data['in_time']:
            time_str = data['in_time']
            # Handle potential seconds in time string (HH:MM:SS)
            if len(time_str.split(':')) == 3:
                time_str = time_str[:5]
            record.in_time = datetime.strptime(time_str, '%H:%M').time()
        
        if 'out_time' in data and data['out_time']:
            time_str = data['out_time']
            # Handle potential seconds in time string (HH:MM:SS)
            if len(time_str.split(':')) == 3:
                time_str = time_str[:5]
            record.out_time = datetime.strptime(time_str, '%H:%M').time()
            
        db.session.commit()

        return record

