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

  def __str__(self):
    return f"name: {self.name}\ngender: {self.gender}\nsalary: {self.salary}"

@app.route('/employee', methods=['GET'])
def get_employees():
  emp = Employee.query.all()
  return jsonify(emp)


if __name__ == '__main__':
  app.run(debug=True)
