from apps.database import db
from apps.models import Student
from flask import Blueprint, request, jsonify, abort


studentBP = Blueprint('student', __name__, "/students/")
@studentBP.route('/', methods=['GET'])
def get_students():
    stu = Student.query.all()
    return jsonify([s.to_dict() for s in stu])


@studentBP.route('/<int:id>',methods=['GET'])
def get_student(id):
    ...

@studentBP.route('/', methods=['POST'])
def insert_student():
    if not request.json or not all(x in request.json for x in ('name', 'email', 'enrolled_data')):
        abort(400)
    stu_info = Student(request.json['name'], request.json['email'])
    db.session.add(stu_info)
    db.commit()

    return jsonify("New Studenr Enrolled!")


