from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1130@localhost/EmployeeManagement'

db = SQLAlchemy(app)
class Employee(db.Model):
    """
    Creating one table using ORM
    """

    __tablename__ = 'Employee'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    salary = db.Column(db.Numeric(10, 2), nullable=False)


    # Constructor
    def __init__(self, name='', gender='', salary=''):
          self.name = name
          self.salary = salary
          self.gender = gender


    def to_dict(self):
        return {
              'id': self.id,
              'name': self.name,
              'gender': self.gender,
              'salary': str(self.salary)
          }

@app.route('/employee', methods=['GET'])
def get_employees():
    emp = Employee.query.all()
    return jsonify([e.to_dict() for e in emp])

@app.route('/employee/<int:id>', methods=['GET'])
def get_employee(id):
    emp = Employee.query.get(id)
    if emp is None:
        abort(404)
    
    return jsonify(emp.to_dict())

@app.route('/employee', methods=['POST'])
def insert_emp():
    if not request.json or not all(k in request.json for k in ('name', 'gender', 'salary')):
        abort(400) # refer to bad request

    emp_info = Employee(request.json['name'],request.json['gender'], request.json['salary'])
    db.session.add(emp_info)
    db.session.commit()

    return jsonify("Employer inserted!")


@app.route('/employee/<int:id>', methods=['PUT'])
def update_emp(id):
    if not request.json or not request.json['salary']:
        abort(400)
    emp = Employee.query.get(id)
    if emp is None:
        abort(404)
    emp.salary = request.json['salary']
    db.session.commit()
    return jsonify(emp.to_dict())

@app.route('/employee/<int:id>', methods=['DELETE'])
def delete_emp(id):
    emp = Employee.query.get(id)
    if emp is None:
        abort(404, description='Employee not found')
    db.session.delete(emp)
    db.session.commit()

    return jsonify('Employee was removed')

if __name__ == '__main__':
  app.run(debug=True)
