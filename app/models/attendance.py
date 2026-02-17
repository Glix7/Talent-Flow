"""
Attendance Model definition.
"""
from datetime import datetime
from app.extensions import db

class Attendance(db.Model):
    """
    Attendance model to track employee check-ins/outs.
    """
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    in_time = db.Column(db.Time, nullable=True)
    out_time = db.Column(db.Time, nullable=True)
    status = db.Column(db.String(20), default='Present')  # Present, Absent, etc.

    def to_dict(self):
        """
        Convert to dictionary.
        """
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'date': self.date.isoformat() if self.date else None,
            'in_time': self.in_time.isoformat() if self.in_time else None,
            'out_time': self.out_time.isoformat() if self.out_time else None,
            'status': self.status
        }

    def __repr__(self):
        return f'<Attendance Emp:{self.employee_id} Date:{self.date}>'
