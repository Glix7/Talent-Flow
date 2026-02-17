"""
Employee Model definition.
"""
from datetime import datetime
from app.extensions import db

class Employee(db.Model):
    """
    Employee model for storing staff details.
    """
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    designation = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    date_of_joining = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    attendance_records = db.relationship('Attendance', backref='employee', lazy=True)

    def to_dict(self):
        """
        Convert object to dictionary for API response.
        """
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'designation': self.designation,
            'department': self.department,
            'date_of_joining': self.date_of_joining.isoformat() if self.date_of_joining else None,
            'created_at': self.created_at.isoformat()
        }

    def __repr__(self):
        return f'<Employee {self.name}>'
