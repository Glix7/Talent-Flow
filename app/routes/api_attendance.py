"""
API endpoints for Attendance tracking.
"""
from flask import jsonify, request
from . import blueprint
from app.services.attendance_service import AttendanceService

@blueprint.route('/api/attendance/mark', methods=['POST'])
def mark_attendance():
    """
    Mark attendance (in/out) for an employee.
    """
    data = request.get_json()
    if not data or not 'employee_id' in data:
        return jsonify({'error': 'Employee ID required'}), 400

    try:
        attendance = AttendanceService.mark_attendance(data)
        return jsonify(attendance.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception:
        return jsonify({'error': 'Failed to mark attendance'}), 500

@blueprint.route('/api/attendance/<int:employee_id>', methods=['GET'])
def get_attendance_history(employee_id):
    """
    Get attendance history for an employee.
    """
    records = AttendanceService.get_attendance_history(employee_id)
    return jsonify([rec.to_dict() for rec in records])
