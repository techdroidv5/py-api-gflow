from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
api = Api(app)

# Fixed credentials (for login)
USERNAME = 'admin'
PASSWORD_HASH = generate_password_hash('password123')  # Secure hashed password

# In-memory data storage for CRUD operations (as an example)
items = []

# Login Resource
class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if username == USERNAME and check_password_hash(PASSWORD_HASH, password):
            return {'message': 'Login successful'}, 200
        else:
            return {'message': 'Invalid credentials'}, 401

# Create Item Resource
class CreateItem(Resource):
    def post(self):
        """ Create a new item """
        data = request.get_json()
        new_item = {
            'id': len(items) + 1,
            'name': data['name'],
            'description': data['description']
        }
        items.append(new_item)
        return new_item, 201

# Get Item Resource
class GetItem(Resource):
    def get(self, item_id):
        """ Get an item by its ID """
        item = next((item for item in items if item['id'] == item_id), None)
        if item:
            return item, 200
        return {'message': 'Item not found'}, 404

# Get All Items Resource
class GetAllItems(Resource):
    def get(self):
        """ Get all items """
        return items, 200

# Update Item Resource
class UpdateItem(Resource):
    def put(self, item_id):
        """ Update an existing item """
        data = request.get_json()
        item = next((item for item in items if item['id'] == item_id), None)
        if item:
            item['name'] = data['name']
            item['description'] = data['description']
            return item, 200
        return {'message': 'Item not found'}, 404

# Delete Item Resource
class DeleteItem(Resource):
    def delete(self, item_id):
        """ Delete an item by its ID """
        global items
        items = [item for item in items if item['id'] != item_id]
        return {'message': 'Item deleted'}, 200

# Add Resources to API with different URL paths
api.add_resource(Login, '/login')
api.add_resource(CreateItem, '/create')
api.add_resource(GetItem, '/get/<int:item_id>')
api.add_resource(GetAllItems, '/get-all')  # New endpoint for getting all items
api.add_resource(UpdateItem, '/update/<int:item_id>')
api.add_resource(DeleteItem, '/delete/<int:item_id>')

if __name__ == '__main__':
    app.run(debug=True)
