from flask import Flask, request, jsonify, abort

app = Flask(__name__)

items = [
  {'id': 1, 'name': "Sarah"},
  {"id": 2, 'name': "Mohamed"}
]

def generate_id():
  num = max(item['id'] for item in items) + 1
  return num

# GET all items
@app.route('/items', methods = ['GET'])
def get_items():
  return jsonify(items)

# GET specific item
@app.route('/items/<int:id>', methods=['GET'])
def get_item(id):
  item = next((x for x in items if x['id'] == id), None)
  if item is None:
    abort(404)
  return jsonify(item)

# POST
@app.route('/items', methods=['POST'])
def create_item():
  if not request.json:
    abort(404)
  item = {
    'id':generate_id(),
    'name': request.json['name']
  }
  items.append(item)
  return jsonify(item)

# PUT => update item
@app.route('/items/<int:id>', methods=['PUT'])
def update_name(id):
  item = next((x for x in items if x['id'] == id), None)
  if item is None:
    abort(404)
  if not request.json:
    abort(400)
  item['name'] = request.json.get('name', item['name'])
  return jsonify(item)

@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = next((x for x in items if x['id'] == id), None)
    if item is None:
        abort(404)
    items.remove(item)
    return jsonify({'result': True})
  

if __name__ == "__main__":
  app.run(debug=True)