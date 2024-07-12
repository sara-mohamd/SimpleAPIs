from flask import Flask, abort, request, jsonify
from mysql.connector import connect
app = Flask(__name__)

try:
    def get_connection():
        connection = connect(
          user='root',
          host='localhost',
          database='EmployeeManagement',
          password='1130',
          ssl_disabled=True
        )
        return connection
except Exception as e:
    print(f'Error: {e}')

def format_file(file):
    ftext = []
    for line in file:
        formatted_line = {
            'id': line[0],
            'Name': line[1],
            'Gender': line[2],
            'Salary': float(line[3]) if line[3] is not None else None  # Convert Decimal to float for JSON serialization
        }
        ftext.append(formatted_line)
    return ftext

# get all emploee
@app.route('/employee', methods=['GET'])
def get_employees():
    with get_connection() as conn, conn.cursor() as cursor:
        cursor.execute('SELECT * FROM Employees')
        employees = cursor.fetchall()
    return jsonify(format_file(employees))


# GET specific employee
@app.route('/employee/<int:id>', methods=['GET'])
def get_employee(id):
    try:
          with get_connection() as conn, conn.cursor() as cursor:
            cursor.execute('SELECT * FROM Employees WHERE id=%s', (id,))
            emp = cursor.fetchone()
        
          if not emp:
            abort(404)
          md = {
                'id':emp[0],
                'name':emp[1],
                'gender':emp[2],
                'salary':float(emp[3])
                }
          return jsonify(md)
    except Exception as e:
        return f'Exception: {e}'
    
    

if __name__ == '__main__':
    app.run(debug=True)
