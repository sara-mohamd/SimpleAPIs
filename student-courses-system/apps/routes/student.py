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
    emp = Student.query.get(id)
    if emp is None:
        abort(404)

    return jsonify(emp.to_dict())

@studentBP.route('/', methods=['POST'])
def insert_student():
    if not request.json or not all(x in request.json for x in ('name', 'email')):
        abort(400)
    stu_info = Student(request.json['name'], request.json['email'])
    db.session.add(stu_info)
    db.session.commit()
    return jsonify("New Studenr Enrolled!")

@studentBP.route('/<int:id>', methods=['PUT'])
def update_email(id):
    stu = Student.query.get(id)
    if stu is None:
        abort(404, description="email is empty")
    if not request.json or not request.json['email']:
        abort(400, description='There is no either request message or email included!')
    stu.email = request.json['email']
    db.session.commit()
    return jsonify(stu.to_dict())


@studentBP.route('/<int:id>', methods=['DELETE'])
def delete_stu(id):
    stu = Student.query.get(id)
    if stu is None:
        abort(404, description='Student not found')
    db.session.delete(stu)
    db.session.commit()
    return jsonify('Student was removed')
