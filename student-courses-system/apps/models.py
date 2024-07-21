from apps.database import db
from datetime import datetime

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    enrolled_date = db.Column(db.Date, default=datetime.utcnow)


    def __init__(self, name, email):
        self.name = name
        self.email = email


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'enrolled_date': self.enrolled_date
        }

    


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(255), nullable=False)
    course_code = db.Column(db.String(50), unique=True, nullable=False)  # Ensure course_code is unique
    credits = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'course_name': self.course_name,
            'course_code': self.course_code,
            'credits': self.credits
        }

class Student_Courses(db.Model):
    __tablename__ = "student_courses"
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), primary_key=True)

    student = db.relationship('Student', backref=db.backref('enrollments', cascade='all, delete-orphan'))
    course = db.relationship('Course', backref=db.backref('enrollments', cascade='all, delete-orphan'))